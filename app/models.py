from app.app import db


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    content = db.Column(db.UnicodeText, nullable=False)
    answer = db.Column(db.UnicodeText)

    def __serialize__(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'answer': self.answer
        }


def serialize(obj):
    if obj is None:
        return jsonify(None)

    if not hasattr(obj, '__serialize__'):
        raise TypeError(
            'Object is not serializable. Object must have a __serialize__ function.')
    return obj.__serialize__()
