from app.app import db
from app.models import questions_categories


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    categories = db.relationship(
        'Category', secondary=questions_categories, backref='questions')
    hints = db.relationship('Hint', backref='question')
    answers = db.relationship('Answer')

    def update(self, **args):
        for key in args:
            setattr(self, key, args[key])
        return self

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'categories': [category.name for category in self.categories],
            'hints': [{'id': hint.id, 'content': hint.content} for hint in self.hints],
            'answers': [{'id': answer.id, 'content': answer.content} for answer in self.answers]
        }
