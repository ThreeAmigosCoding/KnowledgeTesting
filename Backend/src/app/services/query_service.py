from SPARQLWrapper import SPARQLWrapper, JSON
from ..utils.queries import *

sparql_endpoint = "http://localhost:8890/sparql"  # Replace with your Virtuoso SPARQL endpoint
sparql = SPARQLWrapper(sparql_endpoint)

def average_scores(first_name=None, last_name=None, min_avg_score=None, max_avg_score=None):

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
    print(final_query)

    sparql.setQuery(final_query)
    sparql.setReturnFormat(JSON)
    try:
        # Execute the query
        results = sparql.query().convert()

        # Process and print the results
        for result in results["results"]["bindings"]:
            student = result.get("student", {}).get("value", "N/A")
            first_name = result.get("firstName", {}).get("value", "N/A")
            last_name = result.get("lastName", {}).get("value", "N/A")
            tests_taken = result.get("testsTaken", {}).get("value", "N/A")
            avg_score = result.get("avgScorePercent", {}).get("value", "N/A")
            best_score = result.get("bestScorePercent", {}).get("value", "N/A")

            print(f"Student: {student}")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Tests Taken: {tests_taken}")
            print(f"Average Score (%): {avg_score}")
            print(f"Best Score (%): {best_score}")
            print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}")
    pass