from flask import Blueprint, request, jsonify
from app.models import Category
from app.app import db
from .util import all_response, specific_response
from sqlalchemy.exc import IntegrityError

categories_blueprint = Blueprint('category', __name__)


@categories_blueprint.route('', methods=['GET'])
def get_categories():
    if request.method == 'POST':
        return post_question()

    return all_response(Category, 'categories')


@categories_blueprint.route('/<string:category_name>', methods=['GET'])
def get_category_specific(category_name):
    return specific_response(Category, 'name', category_name)


@categories_blueprint.route('', methods=['POST'])
def post_category():
    try:
        category = Category()
        category.name = request.json['name']
        db.session.add(category)
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
    except IntegrityError as err:
        print(err.args)
        response = jsonify(
            {'message': 'Category already exists.'})
        response.status_code = 409
        return response
