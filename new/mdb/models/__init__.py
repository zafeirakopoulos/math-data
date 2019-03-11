from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, RoleMixin, UserMixin, Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate

db = SQLAlchemy()
user_datastore = None
security = None

# Define models
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User {self.email} - {self.roles}>"

    def to_dict(self) -> dict:
        d_out = dict((key, val) for key, val in self.__dict__.items())
        d_out.pop("_sa_instance_state", None)
        d_out["_id"] = d_out.pop("id", None)  # rename id key to interface with response
        return d_out

def construct_app(app):
    db = SQLAlchemy(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Migrate(app, db)
    security = Security(app, user_datastore)
    return app
