import os

from flask import Flask

from online_election import create_config
from online_election import error
from online_election import index
from .user_management import register, login, voterHome, adminHome
from .voting_management import adminElection, elections


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.urandom(24)
    # create_config.CreateConfigParse().add_keys()
    app.register_blueprint(register.bp, url_prefix="/register")
    app.register_blueprint(login.bp, url_prefix="/login")
    app.register_blueprint(voterHome.bp, url_prefix="/voterHome")
    app.register_blueprint(adminElection.bp, url_prefix="/adminElection")
    app.register_blueprint(elections.bp, url_prefix="/elections")
    app.register_blueprint(index.bp, url_prefix="/")
    app.register_blueprint(adminHome.bp, url_prefix="/adminHome")
    app.register_blueprint(error.bp, url_prefix="/")

    return app
