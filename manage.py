#!/usr/bin/env python3

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from md import create_app
from md.models import db, user_datastore
from flask_security.utils import hash_password

# sets up the app
app, db, user_datastore = create_app()

manager = Manager(app)
#migrate = Migrate(app, db)

# adds the python manage.py db init, db migrate, db upgrade commands
manager.add_command("db", MigrateCommand)


@manager.command
def runserver():
    app.run(debug=True, host="0.0.0.0", port=5000)


@manager.command
def runworker():
    app.run(debug=False)

#
# @manager.command
# def recreate_db():
#     """
#     Recreates a database. This should only be used once
#     when there's a new database instance. This shouldn't be
#     used when you migrate your database.
#     """
#
#     pass


if __name__ == "__main__":
    manager.run()
