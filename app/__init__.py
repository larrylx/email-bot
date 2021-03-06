from flask import Flask

from gmail import gmail_api_bp


def create_flask_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)

    # Register Gmail API Blue Print
    app.register_blueprint(gmail_api_bp)

    return app
