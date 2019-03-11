import os
import logging

from flask import Flask, request
from flask_cors import CORS
from sqlalchemy_utils import create_database, database_exists
from flask_bootstrap import Bootstrap

from mdb.config import config
from mdb.core import all_exception_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


# why we use application factories http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
def create_app(test_config=None):
    """
    The flask application factory. To run the app somewhere else you can:
    ```
    from api import create_app
    app = create_app()

    if __main__ == "__name__":
        app.run()
    """
    app = Flask(__name__)

    CORS(app)  # add CORS

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    # for configuration options, look at api/config.py
    if test_config:
        # purposely done so we can inject test configurations
        # this may be used as well if you'd like to pass
        # in a separate configuration although I would recommend
        # adding/changing it in api/config.py instead
        # ignore environment variable config if config was given
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
        print("GOING IN")
        if not database_exists(db_url):
            print("!!! ITS IN !!!")
            create_database(db_url)

    # register sqlalchemy to this app
    from mdb.models import construct_app
    app = construct_app(app)    
    Bootstrap(app)

    # import and register blueprints
    from mdb.views.home import home_app
    from mdb.views.data import data_app
    from mdb.views.formatter import formatter_app

    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(home_app)
    app.register_blueprint(data_app, url_prefix="/data")
    #app.register_blueprint(formatter_app, url_prefix="/formatter")

    # register error Handler
    app.register_error_handler(Exception, all_exception_handler)

    return app
