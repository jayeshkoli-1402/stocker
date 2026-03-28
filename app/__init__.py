from flask import Flask
from .routes import route_bp

def CREATE_APP():
    app = Flask(__name__)
    app.register_blueprint(route_bp)
    app.secret_key = "supersecret"


    return app