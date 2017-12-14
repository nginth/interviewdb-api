from flask import Flask


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)

    return app
