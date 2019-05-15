
import os
#from mdb.core import get_pg_url

# more configuration options here http://flask.pocoo.org/docs/1.0/config/
class Config:
    SECRET_KEY = "testkey"
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_PASSWORD_SALT = "fhasdgihwntlgy8f"
    #SECURITY_PASSWORD_HASH = "plaintext"
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('user_name', 'email')
    LOG_FILE = "api.log"
    FLASK_ADMIN_SWATCH = "cosmo"


class DevelopmentConfig(Config):
    '''
    url = (
        get_pg_url()
        if get_pg_url()
        else "postgresql://testusr:password@127.0.0.1:5432/testdb"  # TODO set the URI to get_pg_url() once you have `creds.ini` setup
    )
    SQLALCHEMY_DATABASE_URI = url'''
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )  # you may do the same as the development config
    DEBUG = False


class DockerDevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://testusr:password@postgres/testdb"
    DEBUG = True


config = {"dev": DevelopmentConfig, "prod": ProductionConfig, "docker": DockerDevConfig}
