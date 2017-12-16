from flask import Blueprint, request, jsonify
from app.models import Answer
from app.app import db

answers_blueprint = Blueprint('answer', __name__)


@answers_blueprint.route('', methods=['POST'])
def post_answer():
    try:
        new_answer = answer_from_json(request.get_json())
        db.session.add(new_answer)
        db.session.commit()
        response = jsonify({'message': 'Created.'})
        response.status_code = 201
        return response
    except KeyError as err:
        print(err.args)
        response = jsonify(
            {'message': 'Bad request. Request must contain field: ' + err.args[0] + '.'})
        response.status_code = 400
        return response


def answer_from_json(json):
    answer = Answer()
    answer.content = json['content']
    answer.question_id = json['questionId']
    return answer
