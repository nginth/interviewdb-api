from app.app import db


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    version = db.Column(db.UnicodeText, nullable=False)

    def __serialize__(self):
        return {'id': self.id, 'name': self.name, 'version': self.version}
