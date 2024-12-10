import pandas as pd
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from learning_spaces.kst import iita

from ..models import db, Graph, Node, Edge, Result, Answer, StudentAnswer, Question, Test
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
    graphs = Graph.query.all()  # TODO add filtering by author id
    graph_schema = GraphSchema(many=True)
    return jsonify(graph_schema.dump(graphs))


def get_graph_by_test_id(test_id):
    graph_id = Test.query.with_entities(Test.graph_id).filter_by(id=test_id).scalar()
    graph = Graph.query.filter(Graph.id == graph_id).first()
    graph_schema = GraphSchema(many=False)
    return jsonify(graph_schema.dump(graph)), 200


def get_generated_graphs(related_graph_id):
    graphs = Graph.query.filter(Graph.related_graph_id == related_graph_id).all()
    graph_schema = GraphSchema(many=True)
    return jsonify(graph_schema.dump(graphs)), 200


def create_knowledge_matrix(test_id):
    results = Result.query.filter_by(test_id=test_id, is_used=False).all()

    questions = Question.query.filter_by(test_id=test_id).all()
    node_map = {question.id: question.node_id for question in questions}

    unique_nodes = list(set(node_map.values()))
    node_index_map = {node_id: index for index, node_id in enumerate(unique_nodes)}

    knowledge_matrix = []
    for result in results:
        result.is_used = True
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

            correct_answers_ids = [answer.id for answer in
                                   Answer.query.filter_by(question_id=question_id, is_correct=True)]
            if set(correct_answers_ids) == set(selected_answer_ids):
                student_row[node_index_map[node_id]] = 1

        knowledge_matrix.append(student_row)

    db.session.commit()
    return knowledge_matrix, node_index_map


def analyze_responses(matrix, node_index_map):
    df = pd.DataFrame(matrix, columns=[f"Node_{i}" for i in range(len(matrix[0]))])

    response = iita(df, v=1)

    index_to_node_id = {index: node_id for node_id, index in node_index_map.items()}

    relations = [
        (index_to_node_id[int(rel[0])], index_to_node_id[int(rel[1])])
        for rel in response['implications']
    ]

    return relations


def create_graph_from_relations(relations, test_id):
    related_graph_id = Test.query.with_entities(Test.graph_id).filter_by(id=test_id).scalar()
    new_graph = Graph(title="Demo", related_graph_id=related_graph_id)
    db.session.add(new_graph)
    db.session.flush()

    new_nodes = {}

    for source_id, target_id in relations:
        if source_id not in new_nodes:
            old_node = Node.query.get(source_id)
            new_node = Node(title=old_node.title, graph_id=new_graph.id)
            db.session.add(new_node)
            db.session.flush()
            new_nodes[source_id] = new_node

        if target_id not in new_nodes:
            old_node = Node.query.get(target_id)
            new_node = Node(title=old_node.title, graph_id=new_graph.id)
            db.session.add(new_node)
            db.session.flush()
            new_nodes[target_id] = new_node

    direct_relations = set(relations)
    for intermediate in new_nodes.keys():
        for source_id, target_id in relations:
            if (source_id, intermediate) in direct_relations and (intermediate, target_id) in direct_relations:
                direct_relations.discard((source_id, target_id))

    for source_id, target_id in direct_relations:
        edge = Edge(
            source_id=new_nodes[source_id].id,
            target_id=new_nodes[target_id].id,
            graph_id=new_graph.id
        )
        db.session.add(edge)

    db.session.commit()

    return new_graph


def generate_real_graph(test_id):
    matrix, node_index_map = create_knowledge_matrix(test_id)

    relations = analyze_responses(matrix, node_index_map)

    create_graph_from_relations(relations, test_id)

