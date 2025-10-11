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


def get_teacher_tests_by_context(teacher_email):
    final_query = test_from_teacher_by_context_query.format(teacherEmail=teacher_email)
    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            item = {
                "context": result.get("context", {}).get("value", None),
                "test_count": result.get("testsCount", {}).get("value", None),
            }
            output.append(item)
        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def get_teacher_tests_by_language(teacher_email):
    final_query = test_from_teacher_by_language_query.format(teacherEmail=teacher_email)
    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            item = {
                "language": result.get("language", {}).get("value", None),
                "test_count": result.get("testCount", {}).get("value", None),
            }
            output.append(item)
        return output
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def get_top_10_from_teacher(teacher_email):
    final_query = top_10_from_teacher_query.format(teacherEmail=teacher_email)
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
                "avg_score_percent": result.get("avgScorePercent", {}).get("value", None),
            }
            output.append(item)

        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
    
def prerequisite_mastery(payload: dict):
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    topic = payload.get("topic")
    weak_prerequisites = payload.get("weak_prerequisites")
    
    filters = []
    
    if first_name:
        filters.append(f'FILTER(LCASE(?firstName) = LCASE("{first_name}"))')
    if last_name:
        filters.append(f'FILTER(LCASE(?lastName) = LCASE("{last_name}"))')
    if topic:
        filters.append(f'FILTER(LCASE(STR(?targetNodeName)) = LCASE("{topic}"))')
    if weak_prerequisites:
        filters.append(f'FILTER(LCASE(?weakPrerequisites) = LCASE("{weak_prerequisites}"))')
        
    filter_clause = " ".join(filters) if filters else ""
    final_query = prerequisite_mastery_query.format(filters=filter_clause)

    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()

        output = []
        for result in results["results"]["bindings"]:
            item = {
                "first_name": result.get("firstName", {}).get("value", None),
                "last_name": result.get("lastName", {}).get("value", None),
                "topic": result.get("topic", {}).get("value", None),
                "weak_prerequisites": result.get("weakPrerequisites", {}).get("value", None),
                "avg_topic_performance": result.get("avgTopicPerformance", {}).get("value", None),
                "avg_prereq_performance": result.get("avgPrereqPerformance", {}).get("value", None),
                "prerequisites_count": result.get("prerequisitesCount", {}).get("value", None),
            }
            output.append(item)

        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    

def get_top_worst_fields(teacher_email):
    final_query = top_worst_fields_query.format(teacherEmail=teacher_email)
    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            item = {
                "node" : result.get("node", {}).get("value", None),
                "field" : result.get("nodeTitle", {}).get("value", None),
                "test_title" : result.get("testTitle", {}).get("value", None),
                "incorrect_answers" : result.get("incorrectAnswers", {}).get("value", None),
                "difficulty" : result.get("difficulty", {}).get("value", None).capitalize(),
            }
            output.append(item)
        return output
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def difficulty_performance_analysis(payload: dict):
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    graph_title = payload.get("graph_title")

    filters = []

    if first_name:
        filters.append(f'FILTER(LCASE(?firstName) = LCASE("{first_name}"))')
    if last_name:
        filters.append(f'FILTER(LCASE(?lastName) = LCASE("{last_name}"))')
    if graph_title:
        filters.append(f'FILTER(LCASE(?graphTitle) = LCASE("{graph_title}"))')

    filter_clause = " ".join(filters) if filters else ""
    final_query = difficulty_performance_analysis_query.format(filters=filter_clause)

    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        output = []
        for result in results["results"]["bindings"]:
            item = {
                "first_name": result.get("firstName", {}).get("value", None),
                "last_name": result.get("lastName", {}).get("value", None),
                "graph_title": result.get("graphTitle", {}).get("value", None),
                "very_easy_performance": result.get("veryEasyPerformance", {}).get("value", None),
                "easy_performance": result.get("easyPerformance", {}).get("value", None),
                "medium_performance": result.get("mediumPerformance", {}).get("value", None),
                "difficult_performance": result.get("difficultPerformance", {}).get("value", None),
                "tests_taken": result.get("testsTaken", {}).get("value", None)
            }
            output.append(item)

        return output

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}