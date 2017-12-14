from flask import Blueprint

questions_blueprint = Blueprint('questions', __name__)


@questions_blueprint.route('/')
def get_questions():
    return "Hello"
