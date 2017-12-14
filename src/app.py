from Flask import flask


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)

    return app
