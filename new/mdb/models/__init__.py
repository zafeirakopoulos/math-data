from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, RoleMixin, UserMixin, Security, SQLAlchemyUserDatastore, current_user
from flask_migrate import Migrate
from flask_security.utils import hash_password
from flask_security.forms import RegisterForm, LoginForm, Required
from flask import url_for, redirect, render_template, request, abort
from wtforms import StringField
from flask import current_app as app
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import Admin, AdminIndexView
from flask_admin import helpers as admin_helpers

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
    user_name = db.Column(db.String(31), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(31))
    last_name = db.Column(db.String(31))
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

class ExtendedRegisterForm(RegisterForm):
    user_name = StringField('Username', [Required()])
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])

class ExtendedLoginForm(LoginForm):
    email = StringField('Username or Email', [Required()])

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        #return True
        return current_user and current_user.has_role('admin')
    
    #def _handle_view(self, name, **kwargs):
    #    return redirect(url_for('security.login', next=request.url)) # login

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        #return True
        # current_user.is_authenticated() and 
        return current_user and current_user.has_role('admin')

    #def _handle_view(self, name, **kwargs):
    #    return redirect(url_for('security.login', next=request.url)) # login

def construct_app():
    db.init_app(app)
    db.app = app
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Migrate(app, db)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)

    #db.drop_all()
    db.create_all()

    if not User.query.first():
        user_datastore.find_or_create_role(name='admin', description='Admin of the Mathdata.')
        user_datastore.find_or_create_role(name='editor', description='Editor for the Mathdata. Can review and accept changes.')
        user_datastore.find_or_create_role(name='user', description='Ordinary user.')
        user_datastore.create_user(email='admin@admin.com', user_name='admin', password=hash_password('admin'))
        user_datastore.add_role_to_user('admin@admin.com', 'admin')

        user_datastore.create_user(email='editor@editor.com', user_name='editor', password=hash_password('editor'))
        user_datastore.add_role_to_user('editor@editor.com', 'editor')

        user_datastore.create_user(email='user@user.com', user_name='user', password=hash_password('user'))
        user_datastore.add_role_to_user('user@user.com', 'user')

        db.session.commit()
        print("committing...")

    # Add model views
    admin = Admin(app, name='Mathdata Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(RolesUsers, db.session))

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )


    return db, user_datastore
