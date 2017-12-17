from flask import Blueprint
from app.models import Category
from .util import all_response, specific_response, post_response

categories_blueprint = Blueprint('category', __name__)


@categories_blueprint.route('', methods=['GET'])
def get_categories():
    return all_response(Category, 'categories')


@categories_blueprint.route('', methods=['POST'])
def post_category():
    return post_response(category_from_json)


@categories_blueprint.route('/<string:category_name>', methods=['GET'])
def get_category_specific(category_name):
    return specific_response(Category, 'name', category_name)


def category_from_json(json):
    category = Category()
    category.name = json['name']
    return category
