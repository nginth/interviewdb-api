from flask import Blueprint
from app.models import Answer
from .util import post_response

answers_blueprint = Blueprint('answer', __name__)


@answers_blueprint.route('', methods=['POST'])
def post_answer():
    return post_response(answer_from_json)


def answer_from_json(json):
    answer = Answer()
    answer.content = json['content']
    answer.question_id = json['questionId']
    return answer
