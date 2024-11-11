from flask import Blueprint, request, jsonify
from .services import test_service, graph_service

main = Blueprint('main', __name__)


@main.route('/tests', methods=['GET'])
def get_tests():
    author_id = request.args.get('author_id', type=int)
    if author_id is None:
        return jsonify({"error": "author_id is required"}), 400
    return test_service.get_tests(author_id)


@main.route('/test-questions', methods=['GET'])
def get_test_questions():
    test_id = request.args.get('test_id', type=int)
    if test_id is None:
        return jsonify({"error": "test_id is required"}), 400
    return test_service.get_test_questions(test_id)


@main.route('/test', methods=['GET'])
def get_test_by_id():
    test_id = request.args.get('test_id', type=int)
    if test_id is None:
        return jsonify({"error": "test_id is required"}), 400
    return test_service.get_test_by_id(test_id)


@main.route('/save-graph', methods=['POST'])
def save_graph():
    return graph_service.save_graph(request.json)


@main.route('/create-test', methods=['POST'])
def create_test():
    return test_service.create_test(request.json)
