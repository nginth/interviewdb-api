from flask import Blueprint, request, jsonify
from app.models import Question, Hint
from app.app import db

hints_blueprint = Blueprint('hint', __name__)


@hints_blueprint.route('', methods=['POST'])
def post_hint():
    try:
        new_hint = hint_from_json(request.get_json())
        db.session.add(new_hint)
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


def hint_from_json(json):
    hint = Hint()
    hint.order = json['order']
    hint.content = json['content']
    hint.question_id = json['questionId']
    return hint
