from app.app import db


class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.UnicodeText, primary_key=True)

    def __serialize__(self):
        return {'name': self.name}
