from flask import Blueprint, request, jsonify
from app.models import Question, serialize
from app.app import db

questions_blueprint = Blueprint('questions', __name__)


@questions_blueprint.route('', methods=['GET'])
def get_questions():
    if request.method == 'POST':
        return post_question()

    questions = Question.query.paginate()
    return jsonify({
        'page': questions.page,
        'pages': questions.pages,
        'per_page': questions.per_page,
        'next': questions.next_num,
        'prev': questions.prev_num,
        'questions': [serialize(question) for question in questions.items]
    })


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
            {'message': 'Bad request. Request must contain field: ' + err.args[0] + '.', 'status_code': 400})
        response.status_code = 400
        return response


def question_from_json(json):
    question = Question()
    question.name = json['name']
    question.content = json['content']
    question.answer = json['answer'] if 'answer' in json else None
    return question
