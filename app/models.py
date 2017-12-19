from app.app import db

questions_categories = db.Table('questions_categories',
                                db.Column('question_id', db.Integer, db.ForeignKey(
                                    'question.id'), primary_key=True),
                                db.Column('category_name', db.UnicodeText,
                                          db.ForeignKey('category.name'), primary_key=True)
                                )


def serialize(obj):
    if obj is None:
        return jsonify(None)

    if not hasattr(obj, '__serialize__'):
        raise TypeError(
            'Object is not serializable. Object must have a __serialize__ function.')
    return obj.__serialize__()


from .model.Hint import Hint
from .model.Category import Category
from .model.Language import Language
from .model.Answer import Answer
from .model.Question import Question
