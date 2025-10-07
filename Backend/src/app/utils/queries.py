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
