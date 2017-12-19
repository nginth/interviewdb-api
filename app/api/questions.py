from flask import Blueprint, jsonify, request
from app.models import Question, Category, serialize
from app.app import db
from .util import (all_response,
                   specific_response,
                   post_response,
                   put_response,
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
    return put_response(Question, 'id', question_id, ('hints', 'categories', 'answers'))


@questions_blueprint.route('/<int:question_id>', methods=['GET'])
def get_question_specific(question_id):
    return specific_response(Question, 'id', question_id)


def question_from_json(json):
    question = Question()
    question.name = json['name']
    question.content = json['content']
    question.categories = categories_from_json(json)
    return question


def categories_from_json(json):
    if 'categories' not in json:
        return []
    return Category.query.filter(Category.name.in_(json['categories'])).all()
