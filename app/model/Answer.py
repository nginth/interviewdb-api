from app.app import db


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.UnicodeText, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __serialize__(self):
        return {'id': self.id, 'content': self.content, 'question': self.question_id}
