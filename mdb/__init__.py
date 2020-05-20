import os
import logging

from flask import Flask, request, url_for
from flask_cors import CORS
from sqlalchemy_utils import create_database, database_exists
from flask_bootstrap import Bootstrap
from flask_security import Security, RoleMixin, UserMixin, Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_security.decorators import roles_accepted

from mdb.config import config
from mdb.core import all_exception_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)  # add CORS

    env = os.environ.get("FLASK_ENV", "docker")
    if test_config:
        app.config.from_mapping(**test_config)
    else:
        app.config.from_object(config[env])  # config dict is from api/config.py

    # logging
    formatter = RequestFormatter(
        "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s in [%(module)s: %(lineno)d]: %(message)s"
    )
    if app.config.get("LOG_FILE"):
        fh = logging.FileHandler(app.config.get("LOG_FILE"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    strm = logging.StreamHandler()
    strm.setLevel(logging.DEBUG)
    strm.setFormatter(formatter)

    app.logger.addHandler(strm)
    app.logger.setLevel(logging.DEBUG)

    root = logging.getLogger("core")
    root.addHandler(strm)

    # decide whether to create database

    if env != "prod":
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    Bootstrap(app)

    # import and register blueprints
    from mdb.views.home import home_app
    from mdb.views.data import data_app

    app.register_blueprint(home_app)
    app.register_blueprint(data_app, url_prefix="/data")

    app.register_error_handler(Exception, all_exception_handler)

    from mdb.models import construct_app
    with app.app_context():
        db, user_datastore = construct_app()
        return app, db, user_datastore

    # register error Handler
    # TODO: uncomment this on production
