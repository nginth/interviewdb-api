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
        return not_found()
    return jsonify(serialize(specific_model))


def post_response(from_json):
    try:
        new_model = from_json(request.get_json())
        db.session.add(new_model)
        db.session.commit()
        return created()
    except KeyError as err:
        return bad_request('Bad request. Request must contain field: ' + err.args[0] + '.')
    except IntegrityError as err:
        return bad_request()


def put_response(model, field, match, not_implemented=[]):
    model_to_update = model.query.filter(
        getattr(model, field) == match).first()
    if not model_to_update:
        return not_found()
    update_json = request.get_json()
    if 'id' in update_json:
        return bad_request('Cannot update id.')

    for key in not_implemented:
        if key in update_json:
            return bad_request('Update of ' +
                               key +
                               'not implemented. Use the endpoints respective to ' +
                               key +
                               ' to perform this operation.')

    for key in update_json:
        setattr(model_to_update, key, update_json[key])

    db.session.add(model_to_update)
    db.session.commit()
    return jsonify({
        'message': 'Updated.',
        model.__name__.lower(): serialize(model_to_update)
    })


def not_found(message='Not found.'):
    response = jsonify({'message': message})
    response.status_code = 404
    return response


def bad_request(message='Bad request.'):
    response = jsonify(
        {'message': message})
    response.status_code = 400
    return response


def created(message='Created.'):
    response = jsonify({'message': message})
    response.status_code = 201
    return response
