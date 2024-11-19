from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, Graph, Node, Edge
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