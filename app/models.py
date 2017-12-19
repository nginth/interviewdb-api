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


class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.UnicodeText, primary_key=True)

    def __serialize__(self):
        return {'name': self.name}


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.UnicodeText, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __serialize__(self):
        return {'id': self.id, 'content': self.content, 'question': self.question_id}


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    version = db.Column(db.UnicodeText, nullable=False)

    def __serialize__(self):
        return {'id': self.id, 'name': self.name, 'version': self.version}


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


def serialize(obj):
    if obj is None:
        return jsonify(None)

    if not hasattr(obj, '__serialize__'):
        raise TypeError(
            'Object is not serializable. Object must have a __serialize__ function.')
    return obj.__serialize__()
