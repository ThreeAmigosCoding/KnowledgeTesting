import os

from flask import jsonify, current_app, send_file
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..database import db
from ..models import Test, Question, Answer, Result, StudentAnswer
from ..schemas import TestSchema, QuestionSchema
from ..schemasDTO.in_schemas import TestSchemaInput, TestSubmissionSchemaInput
from .graph_service import generate_real_graph
import xml.etree.ElementTree as ET


def get_tests(author_id):
    tests = Test.query.filter(Test.author_id == author_id).all()
    test_schema = TestSchema(many=True)
    return jsonify(test_schema.dump(tests))


# def get_test_questions(test_id):
#     questions = Question.query.filter(Question.test_id == test_id).all()
#     question_schema = QuestionSchema(many=True)
#     return jsonify(question_schema.dump(questions))


def get_test_by_id(test_id):
    tests = Test.query.filter(Test.id == test_id).first()
    test_schema = TestSchema(many=False)
    return jsonify(test_schema.dump(tests))


def create_test(request_body):
    test_schema = TestSchemaInput()
    try:
        test_data = test_schema.load(request_body)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    test = Test(
        title=test_data['title'],
        author_id=test_data['author_id'],
        graph_id=test_data['graph_id']
    )
    db.session.add(test)
    db.session.flush()

    for question_data in test_data['questions']:
        question = Question(
            text=question_data['text'],
            is_multichoice=question_data['is_multichoice'],
            node_id=question_data['node_id'],
            test_id=test.id
        )
        db.session.add(question)
        db.session.flush()

        for answer_data in question_data['answers']:
            answer = Answer(
                text=answer_data['text'],
                is_correct=answer_data['is_correct'],
                question_id=question.id
            )
            db.session.add(answer)

    try:
        db.session.commit()
        return jsonify(test_schema.dump(test)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def submit_test(request_body):
    schema = TestSubmissionSchemaInput()
    try:
        data = schema.load(request_body)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    test_id = data['test_id']
    student_id = data['student_id']
    answers = data['answers']

    result = Result(test_id=test_id, student_id=student_id)
    db.session.add(result)
    db.session.flush()

    for answer_id in answers:
        student_answer = StudentAnswer(result_id=result.id, answer_id=answer_id)
        db.session.add(student_answer)

    db.session.commit()

    # matrix, node_map = create_knowledge_matrix(test_id)
    # print(f'Matrix: {matrix} \nNode Map: {node_map}')
    generate_real_graph(test_id)

    return jsonify({"message": "Test submitted successfully"}), 201


def export_test_to_qti(test_id):
    try:
        test = Test.query.get(test_id)
        questions = test.questions

        qti_ns = "http://www.imsglobal.org/xsd/imsqti_v2p1"
        ET.register_namespace('', qti_ns)

        root = ET.Element("assessmentTest", xmlns=qti_ns, identifier=f"Test_{test_id}", title=test.title)

        for question in questions:
            item = ET.SubElement(root, "assessmentItem",  identifier=f"Question_{question.id}", title=question.text,
                                 adaptive="false", timeDependent="false")

            item_body = ET.SubElement(item, "itemBody")
            max_choices = "1" if not question.is_multichoice else str(len(question.answers))
            choice_interaction = ET.SubElement(item_body, "choiceInteraction",
                                               responseIdentifier=f"RESPONSE_{question.id}", shuffle="true",
                                               maxChoices=max_choices)
            prompt = ET.SubElement(choice_interaction, "prompt")
            prompt.text = question.text

            for answer in question.answers:
                choice = ET.SubElement(choice_interaction, "simpleChoice", identifier=f"Answer_{answer.id}")
                choice.text = answer.text

            response_declaration = ET.SubElement(item, "responseDeclaration", identifier=f"RESPONSE_{question.id}",
                                                 cardinality="multiple" if question.is_multichoice else "single",
                                                 baseType="identifier")
            correct_response = ET.SubElement(response_declaration, "correctResponse")
            for answer in question.answers:
                if answer.is_correct:
                    value = ET.SubElement(correct_response, "value")
                    value.text = f"Answer_{answer.id}"

            item_feedback = ET.SubElement(item, "itemFeedback", identifier="Feedback")
            item_feedback.text = "Correct!" if question.is_multichoice else "Try again!"

        tree = ET.ElementTree(root)
        exports_dir = current_app.config['EXPORTS_DIR']
        file_path = os.path.join(exports_dir, f'{test_id}-QTI.xml')
        tree.write(file_path, xml_declaration=True, encoding="UTF-8")

    except Exception as e:
        raise "Error exporting the file"

def export_test(test_id):
    try:
        exports_dir = current_app.config['EXPORTS_DIR']
        file_path = os.path.join(exports_dir, f"{test_id}-QTI.xml")

        if not os.path.exists(file_path):
            export_test_to_qti(test_id)

        return send_file(file_path, as_attachment=True, download_name=f"{test_id}-QTI.xml",
                         mimetype="application/octet-stream")

    except Exception as e:
        return jsonify({"error": str(e)}), 500