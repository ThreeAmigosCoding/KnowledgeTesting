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

prerequisite_mastery_query = """
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX kst:  <http://example.org/kst#>
    PREFIX dc:   <http://purl.org/dc/elements/1.1/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    SELECT ?firstName
          ?lastName
          (STR(?targetNodeName) as ?topic)
          (GROUP_CONCAT(DISTINCT ?prereqNodeName; separator=", ") as ?weakPrerequisites)
          (ROUND(AVG(?targetCorrectness) * 100) as ?avgTopicPerformance)
          (ROUND(AVG(?prereqCorrectness) * 100) as ?avgPrereqPerformance)
          (COUNT(DISTINCT ?prereqNode) as ?prerequisitesCount)
    WHERE {{
      ?targetNode a kst:Node ;
                  dc:title ?targetNodeName ;
                  kst:belongsToGraph ?graph .
      
      ?edge a kst:Edge ;
            kst:hasSourceNode ?prereqNode ;
            kst:hasTargetNode ?targetNode .
      
      ?prereqNode dc:title ?prereqNodeName .
      
      ?targetQuestion a kst:Question ;
                      kst:mapsToNode ?targetNode ;
                      kst:belongsToTest ?test .
      
      ?prereqQuestion a kst:Question ;
                      kst:mapsToNode ?prereqNode ;
                      kst:belongsToTest ?test .
      
      ?targetStudentAnswer a kst:StudentAnswer ;
                          kst:answersQuestion ?targetQuestion ;
                          kst:selectedAnswer ?targetAnswer ;
                          kst:belongsToResult ?result .
      
      ?targetAnswer kst:isCorrect ?targetCorrect .
      BIND(IF(?targetCorrect, 1.0, 0.0) AS ?targetCorrectness)
      
      ?prereqStudentAnswer a kst:StudentAnswer ;
                          kst:answersQuestion ?prereqQuestion ;
                          kst:selectedAnswer ?prereqAnswer ;
                          kst:belongsToResult ?result .
      
      ?prereqAnswer kst:isCorrect ?prereqCorrect .
      BIND(IF(?prereqCorrect, 1.0, 0.0) AS ?prereqCorrectness)
      
      ?result kst:belongsToStudent ?student .
      ?student foaf:firstName ?firstName ;
              foaf:lastName ?lastName .
              
      {filters}
    }}
    GROUP BY ?firstName ?lastName ?targetNodeName
    HAVING (AVG(?targetCorrectness) < 0.6 && AVG(?prereqCorrectness) < 0.6)
    ORDER BY ?lastName ?firstName ?avgPrereqPerformance 
"""

test_from_teacher_by_context_query = """
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX kst:  <http://example.org/kst#>
    PREFIX lom:  <http://ltsc.ieee.org/rdf/lom/>
    
    SELECT ?context (COUNT(DISTINCT ?test) AS ?testsCount)
    WHERE {{
      {{
        SELECT DISTINCT ?context WHERE {{
          ?anyTest a kst:Test ;
                   lom:context ?context .
        }}
      }}
    
      ?teacher a kst:Teacher ;
               foaf:mbox <mailto:{teacherEmail}> .
    
      OPTIONAL {{
        ?test a kst:Test ;
              kst:hasAuthor ?teacher ;
              lom:context   ?context .
      }}
    }}
    GROUP BY ?context
    ORDER BY ?context
"""

top_10_from_teacher_query = """
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX kst:  <http://example.org/kst#>
    
    SELECT
      ?student
      ?firstName
      ?lastName
      (ROUND(AVG(?scorePercent) * 100) / 100 AS ?avgScorePercent)
    WHERE {{ 
      {{ 
        SELECT
          ?student
          ?firstName
          ?lastName
          ?result
          (IF(COALESCE(?totalQuestions,0) > 0,
              ROUND((xsd:decimal(COALESCE(?correctQuestions,0)) / xsd:decimal(?totalQuestions)) * 10000) / 100,
              0) AS ?scorePercent)
        WHERE {{ 
          # Find the teacher by email
          ?teacher a kst:Teacher ;
                   foaf:mbox <mailto:{teacherEmail}> .
    
          # Find tests authored by the teacher
          ?test a kst:Test ;
                kst:hasAuthor ?teacher .
    
          # Find results for those tests
          ?result a kst:TestResult ;
                  kst:forTest ?test ;
                  kst:belongsToStudent ?student .
    
          # Get student details
          ?student a kst:Student .
          OPTIONAL {{ ?student foaf:firstName ?firstName . }}
          OPTIONAL {{ ?student foaf:lastName  ?lastName  . }}
    
          # Count correct answers per result
          OPTIONAL {{ 
            SELECT ?result (COUNT(DISTINCT ?qCorr) AS ?correctQuestions)
            WHERE {{ 
              ?sa a kst:StudentAnswer ;
                  kst:belongsToResult ?result ;
                  kst:answersQuestion ?qCorr ;
                  kst:selectedAnswer ?ans .
              ?ans kst:isCorrect true .
            }}
            GROUP BY ?result
          }}
    
          # Count total questions per test
          OPTIONAL {{ 
            SELECT ?test (COUNT(DISTINCT ?qAll) AS ?totalQuestions)
            WHERE {{ 
              ?qAll a kst:Question ;
                    kst:belongsToTest ?test .
            }}
            GROUP BY ?test
          }}
        }}
      }}
    }}
    GROUP BY ?student ?firstName ?lastName
    HAVING (COUNT(?result) > 0)  # Ensure students have at least one result
    ORDER BY DESC(?avgScorePercent)
    LIMIT 10
"""