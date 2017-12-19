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
    update_json = request.get_json()
    if 'id' in update_json:
        return bad_request('Cannot update id.')

    if 'content' in update_json:
        hint.content = update_json['content']
    if 'order' in update_json:
        hint.order = update_json['order']
    if 'questionId' in update_json:
        hint.set_question(update_json['questionId'])

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
