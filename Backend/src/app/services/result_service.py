from flask import jsonify
from ..database import db
from ..models import Result
from ..schemas import ResultSchema

from sqlalchemy import desc


def get_results(student_id):
    results = Result.query.filter(Result.student_id == student_id).order_by(desc(Result.timestamp)).all()
    result_schema = ResultSchema(many=True)
    return jsonify(result_schema.dump(results))


def get_result(result_id):
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    schema = ResultSchema()
    response = schema.dump(result)

    return jsonify(response)
