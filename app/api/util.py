from flask import jsonify
from app.models import serialize


def all_response(model):
    models = model.query.paginate()
    return jsonify({
        'page': models.page,
        'pages': models.pages,
        'per_page': models.per_page,
        'next': models.next_num,
        'prev': models.prev_num,
        'questions': [serialize(model) for model in models.items]
    })


def specific_response(model, field, match):
    specific_model = model.query.filter(getattr(model, field) == match).first()
    if not specific_model:
        response = jsonify({'message': 'Not found.'})
        response.status_code = 404
        return response
    return jsonify(serialize(specific_model))
