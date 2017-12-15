from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)
    CORS(app)

    db.init_app(app)
    from app import models
    with app.app_context():
        db.create_all()

    from .api.questions import questions_blueprint
    from .api.categories import categories_blueprint
    app.register_blueprint(questions_blueprint, url_prefix="/question")
    app.register_blueprint(categories_blueprint, url_prefix="/category")

    return app
