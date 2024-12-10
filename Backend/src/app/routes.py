from flask import Blueprint, request, jsonify
from .services import test_service, graph_service, user_service, result_service
from .utils.auth import authorize

main = Blueprint('main', __name__)


@main.route('/tests', methods=['GET'])
def get_tests():
    author_id = request.args.get('author_id', type=int)
    if author_id is None:
        return jsonify({"error": "author_id is required"}), 400
    return test_service.get_tests(author_id)


# @main.route('/test-questions', methods=['GET'])
# def get_test_questions():
#     test_id = request.args.get('test_id', type=int)
#     if test_id is None:
#         return jsonify({"error": "test_id is required"}), 400
#     return test_service.get_test_questions(test_id)


@main.route('/test', methods=['GET'])
def get_test_by_id():
    test_id = request.args.get('test_id', type=int)
    if test_id is None:
        return jsonify({"error": "test_id is required"}), 400
    return test_service.get_test_by_id(test_id)


@main.route('/save-graph', methods=['POST'])
def save_graph():
    return graph_service.save_graph(request.json)


@main.route('/generate-graph', methods=['POST'])
def generate_graph():
    return graph_service.generate_real_graph(request.json)


@main.route('/create-test', methods=['POST'])
def create_test():
    return test_service.create_test(request.json)


@main.route('/get-graphs', methods=['GET'])
def get_graphs():
    return graph_service.get_graphs()


@main.route('/get-graph-by-test-id', methods=['GET'])
def get_graphs_by_test_id():
    test_id = request.args.get('id', type=int)
    if test_id is None:
        return jsonify({"error": "test_id is required"}), 400
    return graph_service.get_graph_by_test_id(test_id)


@main.route('/get-generated-graphs', methods=['GET'])
def get_generated_graphs():
    related_graph_id = request.args.get('assumedGraphId', type=int)
    if related_graph_id is None:
        return jsonify({"error": "related_graph_id is required"}), 400
    return graph_service.get_generated_graphs(related_graph_id)


@main.route('submit-test', methods=['POST'])
def submit_test():
    return test_service.submit_test(request.json)

@main.route('/login', methods=['POST'])
def login():
    return user_service.login(request.json)

@main.route('/register', methods=['POST'])
def register():
    return user_service.register(request.json)

@main.route('get-results', methods=['GET'])
def get_results():
    student_id = request.args.get('studentId', type=int)
    test_id = request.args.get('testId', type=int)
    if (student_id is None and test_id is None) or (test_id is not None and student_id is not None):
        return jsonify({"error": "studentId or testId is required"}), 400
    if student_id:
        return result_service.get_results_by_student_id(student_id)
    return result_service.get_results_by_test_id(test_id)


@main.route('get-result', methods=['GET'])
def get_result():
    result_id = request.args.get('resultId', type=int)
    if result_id is None:
        return jsonify({"error": "resultId is required"}), 400
    return result_service.get_result(result_id)
