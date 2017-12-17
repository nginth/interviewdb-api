from flask import Blueprint, jsonify, request
from app.models import Question, Category, serialize
from app.app import db
from .util import (all_response,
                   specific_response,
                   post_response,
                   not_found,
                   bad_request)

questions_blueprint = Blueprint('question', __name__)


@questions_blueprint.route('', methods=['GET'])
def get_questions():
    return all_response(Question, 'questions')


@questions_blueprint.route('', methods=['POST'])
def post_question():
    return post_response(question_from_json)


@questions_blueprint.route('/<int:question_id>', methods=['PUT'])
def put_question(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    if not question:
        return not_found()
    question_json = request.get_json()
    if 'id' in question_json:
        return bad_request('Cannot update id.')
    for key in ('hints', 'categories', 'answers'):
        if key in question_json:
            return bad_request('Update of ' + key + 'not implemented.')
    # TODO: figure out a better way to do this
    question.name = question_json['name'] if 'name' in question_json else question.name
    question.content = question_json['content'] if 'content' in question_json else question.content

    db.session.add(question)
    db.session.commit()
    return jsonify({
        'message': 'Updated.',
        'question': serialize(question)
    })


@questions_blueprint.route('/<int:question_id>', methods=['GET'])
def get_question_specific(question_id):
    return specific_response(Question, 'id', question_id)


def question_from_json(json):
    question = Question()
    question.name = json['name']
    question.content = json['content']
    question.answer = json['answer'] if 'answer' in json else None
    question.categories = categories_from_json(json['categories'])
    return question


def categories_from_json(categories):
    return Category.query.filter(Category.name.in_(categories)).all()
