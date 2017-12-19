from app.app import db
from app.models import Question
from app.api.util import not_found


class Hint(db.Model):
    __tablename__ = 'hint'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __serialize__(self):
        return {
            'id': self.id,
            'order': self.order,
            'content': self.content,
            'questionId': self.question_id
        }

    def set_question(self, question_id):
        question = Question.query.filter(
            Question.id == question_id).first()
        if not question:
            return not_found('Question with id ' + question_id + ' not found.')
        self.question = question
