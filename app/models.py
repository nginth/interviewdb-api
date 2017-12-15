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
    answer = db.Column(db.UnicodeText)
    categories = db.relationship(
        'Category', secondary=questions_categories, backref='questions')

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'answer': self.answer,
            'categories': [category.name for category in self.categories]
        }


def serialize(obj):
    if obj is None:
        return jsonify(None)

    if not hasattr(obj, '__serialize__'):
        raise TypeError(
            'Object is not serializable. Object must have a __serialize__ function.')
    return obj.__serialize__()


class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.UnicodeText, primary_key=True)

    def __serialize__(self):
        return {
            'name': self.name
        }
