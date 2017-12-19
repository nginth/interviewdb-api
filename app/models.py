from app.app import db

questions_categories = db.Table('questions_categories',
                                db.Column('question_id', db.Integer, db.ForeignKey(
                                    'question.id'), primary_key=True),
                                db.Column('category_name', db.UnicodeText,
                                          db.ForeignKey('category.name'), primary_key=True)
                                )


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    categories = db.relationship(
        'Category', secondary=questions_categories, backref='questions')
    hints = db.relationship('Hint', backref='question')
    answers = db.relationship('Answer')

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'categories': [category.name for category in self.categories],
            'hints': [{'id': hint.id, 'content': hint.content} for hint in self.hints],
            'answers': [{'id': answer.id, 'content': answer.content} for answer in self.answers]
        }


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
