from flask import request, jsonify
from app.models import serialize
from app.app import db
from sqlalchemy.exc import IntegrityError


def all_response(model, model_name):
    models = model.query.paginate()
    return jsonify({
        'page': models.page,
        'pages': models.pages,
        'per_page': models.per_page,
        'next': models.next_num,
        'prev': models.prev_num,
        model_name: [serialize(model) for model in models.items]
    })


def specific_response(model, field, match):
    specific_model = model.query.filter(getattr(model, field) == match).first()
    if not specific_model:
        response = jsonify({'message': 'Not found.'})
        response.status_code = 404
        return response
    return jsonify(serialize(specific_model))


def post_response(from_json):
    try:
        new_model = from_json(request.get_json())
        db.session.add(new_model)
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
            {'message': 'Bad request.'})
        response.status_code = 400
        return response
