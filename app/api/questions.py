from flask import Blueprint, request, jsonify
from app.models import Question, Category
from app.app import db
from .util import all_response, specific_response

questions_blueprint = Blueprint('question', __name__)


@questions_blueprint.route('', methods=['GET'])
def get_questions():
    if request.method == 'POST':
        return post_question()

    return all_response(Question, 'questions')


@questions_blueprint.route('/<int:question_id>', methods=['GET'])
def get_question_specific(question_id):
    return specific_response(Question, 'id', question_id)


@questions_blueprint.route('', methods=['POST'])
def post_question():
    try:
        new_question = question_from_json(request.get_json())
        db.session.add(new_question)
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


def question_from_json(json):
    question = Question()
    question.name = json['name']
    question.content = json['content']
    question.answer = json['answer'] if 'answer' in json else None
    question.categories = categories_from_json(json['categories'])
    return question


def categories_from_json(categories):
    return Category.query.filter(Category.name.in_(categories)).all()
