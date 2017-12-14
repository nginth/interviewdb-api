from flask import Flask


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)

    from .api.questions import questions_blueprint
    app.register_blueprint(questions_blueprint, url_prefix="/questions")

    return app
