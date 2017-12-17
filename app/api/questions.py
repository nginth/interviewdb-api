from flask import Blueprint
from app.models import Question, Category
from .util import all_response, specific_response, post_response

questions_blueprint = Blueprint('question', __name__)


@questions_blueprint.route('', methods=['GET'])
def get_questions():
    return all_response(Question, 'questions')


@questions_blueprint.route('', methods=['POST'])
def post_question():
    return post_response(question_from_json)


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
