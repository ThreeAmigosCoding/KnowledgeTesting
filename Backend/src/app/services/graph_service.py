from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from ..models import db, Graph, Node, Edge, Result, Answer, StudentAnswer, Question
from ..schemasDTO.in_schemas import GraphSchemaInput
from ..schemas import GraphSchema

def save_graph(request_body):
    graph_schema = GraphSchemaInput()
    graph_data = graph_schema.load(request_body)

    graph = Graph(title=graph_data['title'])
    db.session.add(graph)
    db.session.flush()

    title_to_node = {}
    for node_data in graph_data['nodes']:
        node = Node(title=node_data['title'], graph=graph)
        db.session.add(node)
        title_to_node[node.title] = node
    db.session.flush()

    for edge_data in graph_data['edges']:
        source_title = edge_data['source']['title']
        target_title = edge_data['target']['title']

        source_node = title_to_node.get(source_title)
        target_node = title_to_node.get(target_title)

        if source_node and target_node:
            edge = Edge(source_id=source_node.id, target_id=target_node.id, graph=graph)
            db.session.add(edge)
        else:
            return jsonify({"error": "Invalid edge data"}), 400

    try:
        db.session.commit()
        return jsonify(graph_schema.dump(graph)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def get_graphs():
    graphs = Graph.query.all() #TODO add filtering by author id
    graph_schema = GraphSchema(many=True)
    return jsonify(graph_schema.dump(graphs))

def create_knowledge_matrix(test_id):

    results = Result.query.filter_by(test_id=test_id).all()

    questions = Question.query.filter_by(test_id=test_id).all()
    node_map = {question.id: question.node_id for question in questions}

    unique_nodes = list(set(node_map.values()))
    node_index_map = {node_id: index for index, node_id in enumerate(unique_nodes)}

    knowledge_matrix = []
    for result in results:
        student_row = [0] * len(unique_nodes)

        student_answers = result.student_answers
        answers_by_question = {}
        for student_answer in student_answers:
            question_id = student_answer.answer.question.id
            if question_id not in answers_by_question:
                answers_by_question[question_id] = []
            answers_by_question[question_id].append(student_answer.answer.id)


        for question_id, selected_answer_ids in answers_by_question.items():
            node_id = node_map[question_id]

            correct_answers_ids = [answer.id for answer in Answer.query.filter_by(question_id=question_id, is_correct=True)]
            print(f'Correct answers: {correct_answers_ids}\nSelected answers: {selected_answer_ids}')
            if set(correct_answers_ids) == set(selected_answer_ids):
                student_row[node_index_map[node_id]] = 1

        knowledge_matrix.append(student_row)

    return knowledge_matrix, node_index_map