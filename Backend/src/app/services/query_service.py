from SPARQLWrapper import SPARQLWrapper, JSON
from ..utils.queries import *

sparql_endpoint = "http://localhost:8890/sparql"
sparql = SPARQLWrapper(sparql_endpoint)

def average_scores(payload: dict):
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    min_avg_score = payload.get("min_avg_score")
    max_avg_score = payload.get("max_avg_score")

    filters = []
    if first_name:
        filters.append(f'FILTER(LCASE(?firstName) = LCASE("{first_name}"))')
    if last_name:
        filters.append(f'FILTER(LCASE(?lastName) = LCASE("{last_name}"))')
    if min_avg_score is not None:
        filters.append(f'FILTER(?avgScorePercent >= {min_avg_score})')
    if max_avg_score is not None:
        filters.append(f'FILTER(?avgScorePercent <= {max_avg_score})')

    filter_clause = " ".join(filters) if filters else ""
    final_query = average_scores_query.format(filters=filter_clause)

    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        output = []
        for result in results["results"]["bindings"]:
            item = {
                "student": result.get("student", {}).get("value", None),
                "first_name": result.get("firstName", {}).get("value", None),
                "last_name": result.get("lastName", {}).get("value", None),
                "tests_taken": result.get("testsTaken", {}).get("value", None),
                "avg_score_percent": result.get("avgScorePercent", {}).get("value", None),
                "best_score_percent": result.get("bestScorePercent", {}).get("value", None),
            }
            output.append(item)

        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
def problematic_topics(payload: dict):
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    graph_title = payload.get("graph_title")
    error_percentage = payload.get("error_percentage")
    
    filters = []

    if first_name:
        filters.append(f'FILTER(LCASE(?firstName) = LCASE("{first_name}"))')
    if last_name:
        filters.append(f'FILTER(LCASE(?lastName) = LCASE("{last_name}"))')
    if graph_title:
        filters.append(f'FILTER(LCASE(?graphTitle) = LCASE("{graph_title}"))')
    if error_percentage is not None:
        filters.append(f'FILTER(?errorPercentage >= {error_percentage})')
        
    filter_clause = " ".join(filters) if filters else ""
    final_query = problematic_topics_query.format(filters=filter_clause)

    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()

        output = []
        for result in results["results"]["bindings"]:
            item = {
                "student": result.get("student", {}).get("value", None),
                "first_name": result.get("firstName", {}).get("value", None),
                "last_name": result.get("lastName", {}).get("value", None),
                "graph_title": result.get("graphTitle", {}).get("value", None),
                "weakest_topic": result.get("weakestTopic", {}).get("value", None),
                "error_count": result.get("errorCount", {}).get("value", None),
                "total_questions": result.get("totalQuestions", {}).get("value", None),
                "error_percentage": result.get("errorPercentage", {}).get("value", None),
            }
            output.append(item)

        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    
    
    