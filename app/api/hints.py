from flask import Blueprint, request, jsonify
from app.models import Hint, Question
from app.app import db
from .util import post_response, put_response, all_response, serialize

hints_blueprint = Blueprint('hint', __name__)


@hints_blueprint.route('', methods=['GET'])
def get_all():
    return all_response(Hint, 'hints')


@hints_blueprint.route('', methods=['POST'])
def create():
    return post_response(hint_from_json)


@hints_blueprint.route('/<int:hint_id>', methods=['PUT'])
def update(hint_id):
    hint = Hint.query.filter(Hint.id == hint_id).first()
    if not hint:
        return not_found()
    hint.update(**request.get_json())
    db.session.add(hint)
    db.session.commit()
    return jsonify({
        'message': 'Updated.',
        'hint': serialize(hint)
    })


def hint_from_json(json):
    hint = Hint()
    hint.order = json['order']
    hint.content = json['content']
    hint.set_question(json['questionId'])
    return hint
