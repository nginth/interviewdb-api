from flask import Blueprint, request, jsonify
from app.models import Category
from app.app import db
from .util import all_response, specific_response

categories_blueprint = Blueprint('category', __name__)


@categories_blueprint.route('', methods=['GET'])
def get_questions():
    if request.method == 'POST':
        return post_question()

    return all_response(Category)


@categories_blueprint.route('/<string:category_name>', methods=['GET'])
def get_question_specific(category_name):
    return specific_response(Category, 'name', category_name)


# @categories_blueprint.route('', methods=['POST'])
# def post_question():
#     try:
#         new_question = question_from_json(request.get_json())
#         db.session.add(new_question)
#         db.session.commit()
#         response = jsonify({'message': 'Created.'})
#         response.status_code = 201
#         return response
#     except KeyError as err:
#         print(err.args)
#         response = jsonify(
#             {'message': 'Bad request. Request must contain field: ' + err.args[0] + '.'})
#         response.status_code = 400
#         return response


# def question_from_json(json):
#     question = Question()
#     question.name = json['name']
#     question.content = json['content']
#     question.answer = json['answer'] if 'answer' in json else None
#     return question
