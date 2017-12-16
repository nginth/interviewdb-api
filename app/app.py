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
    from .api.hints import hints_blueprint
    from .api.answers import answers_blueprint
    app.register_blueprint(questions_blueprint, url_prefix="/question")
    app.register_blueprint(categories_blueprint, url_prefix="/category")
    app.register_blueprint(hints_blueprint, url_prefix="/hint")
    app.register_blueprint(answers_blueprint, url_prefix="/answer")

    return app
