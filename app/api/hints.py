from flask import Blueprint
from app.models import Hint
from .util import post_response

hints_blueprint = Blueprint('hint', __name__)


@hints_blueprint.route('', methods=['POST'])
def post_hint():
    return post_response(hint_from_json)


def hint_from_json(json):
    hint = Hint()
    hint.order = json['order']
    hint.content = json['content']
    hint.question_id = json['questionId']
    return hint
