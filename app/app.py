from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)

    db.init_app(app)
    from app import models
    with app.app_context():
        db.create_all()

    from .api.questions import questions_blueprint
    app.register_blueprint(questions_blueprint, url_prefix="/question")

    return app
