average_scores_query = """
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX kst:  <http://example.org/kst#>
    
    SELECT
      ?student
      ?firstName
      ?lastName
      ?testsTaken
      ?avgScorePercent
      ?bestScorePercent
    WHERE {{
      {{
        SELECT
          ?student
          ?firstName
          ?lastName
          (COUNT(DISTINCT ?result) AS ?testsTaken)
          (ROUND( (AVG(?scorePercent)) * 100 ) / 100 AS ?avgScorePercent)
          (MAX(?scorePercent) AS ?bestScorePercent)
        WHERE {{
          {{
            # ---------- Per-result scoring ----------
            SELECT
              ?student
              ?firstName
              ?lastName
              ?result
              (IF(COALESCE(?totalQuestions,0) > 0,
                  ROUND( (xsd:decimal(COALESCE(?correctQuestions,0)) / xsd:decimal(?totalQuestions)) * 10000 ) / 100,
                  0) AS ?scorePercent)
            WHERE {{
              # TestResult -> Test & Student
              ?result a kst:TestResult ;
                      kst:forTest ?test ;
                      kst:belongsToStudent ?student .
    
              OPTIONAL {{ ?student foaf:firstName ?firstName . }}
              OPTIONAL {{ ?student foaf:lastName  ?lastName  . }}
    
              # Count correctly answered questions per result (distinct by question)
              OPTIONAL {{
                SELECT ?result (COUNT(DISTINCT ?qCorr) AS ?correctQuestions)
                WHERE {{
                  ?sa a kst:StudentAnswer ;
                      kst:belongsToResult ?result ;
                      kst:answersQuestion ?qCorr ;
                      kst:selectedAnswer  ?ans .
                  ?ans kst:isCorrect true .
                }}
                GROUP BY ?result
              }}
    
              # Count total questions per test
              OPTIONAL {{
                SELECT ?test (COUNT(DISTINCT ?qAll) AS ?totalQuestionsSub)
                WHERE {{
                  ?qAll a kst:Question ;
                        kst:belongsToTest ?test .
                }}
                GROUP BY ?test
              }}
    
              BIND(COALESCE(?totalQuestionsSub, 0) AS ?totalQuestions)
            }}
          }}
        }}
        GROUP BY ?student ?firstName ?lastName
      }}
      {filters}
    }}
    ORDER BY ?lastName ?firstName
    """

problematic_topics_query = """
    PREFIX kst: <http://example.org/kst#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?firstName ?lastName ?graphTitle ?weakestTopic ?errorCount ?totalQuestions ?errorPercentage
    WHERE {{
      # Find the specific student
      ?student a kst:Student ;
              foaf:firstName ?firstName ;
              foaf:lastName ?lastName .
      
      {{
        SELECT ?student ?graph ?node (COUNT(*) as ?errorCount) 
        WHERE {{
          ?student a kst:Student .
          
          # Get student's incorrect answers
          ?result kst:belongsToStudent ?student .
          ?studentAnswer kst:belongsToResult ?result ;
                        kst:answersQuestion ?question ;
                        kst:selectedAnswer ?answer .
          ?answer kst:isCorrect false .
          
          # Map to nodes and graphs
          ?question kst:mapsToNode ?node .
          ?node kst:belongsToGraph ?graph .
        }}
        GROUP BY ?student ?graph ?node
      }}
      
      {{
        SELECT ?graph ?node (COUNT(DISTINCT ?q) as ?totalQuestions)
        WHERE {{
          ?q kst:mapsToNode ?node .
          ?node kst:belongsToGraph ?graph .
        }}
        GROUP BY ?graph ?node
      }}
      
      ?graph dc:title ?graphTitle .
      
      ?node dc:title ?topic .
      
      BIND((?errorCount * 100.0 / ?totalQuestions) AS ?errorPercentage)
      
      {{
        SELECT ?student ?graph (MAX(?errorPct) as ?maxErrorPercentage)
        WHERE {{
          {{
            SELECT ?student ?graph ?node (COUNT(*) as ?errCount) 
            WHERE {{
              ?student a kst:Student .
              ?result kst:belongsToStudent ?student .
              ?studentAnswer kst:belongsToResult ?result ;
                            kst:answersQuestion ?question ;
                            kst:selectedAnswer ?answer .
              ?answer kst:isCorrect false .
              ?question kst:mapsToNode ?node .
              ?node kst:belongsToGraph ?graph .
            }}
            GROUP BY ?student ?graph ?node
          }}
          
          {{
            SELECT ?g ?n (COUNT(DISTINCT ?question) as ?totalQ)
            WHERE {{
              ?question kst:mapsToNode ?n .
              ?n kst:belongsToGraph ?g .
            }}
            GROUP BY ?g ?n
          }}
          
          FILTER(?graph = ?g && ?node = ?n)
          BIND((?errCount * 100.0 / ?totalQ) AS ?errorPct)
        }}
        GROUP BY ?student ?graph
      }}
      
      FILTER(?errorPercentage = ?maxErrorPercentage)
      
      BIND(?topic AS ?weakestTopic)
      
      # FILTER(?firstName = "Aleksandar")                    # Filter by first name
      # FILTER(?lastName = "Aleksić")                      # Filter by last name
      # FILTER(?graphTitle = "Prostor znanja - Hemija - Organska hemija")
      # FILTER(?errorPercentage > 20)                    # Error percentage threshold
      {filters}

    }}
    ORDER BY ?firstName ?lastName ?graphTitle DESC(?errorPercentage)
"""