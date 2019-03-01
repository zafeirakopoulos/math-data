from flask import Flask, Blueprint, render_template
from flask_bootstrap import Bootstrap

from mdb.data import data_app
from mdb.formatter import formatter_app

app = Flask("mdb")
Bootstrap(app)

static_definition = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
contact1 = {
    'name': 'Dr. Zaferiakis Zaferiakopoulos',
    'phone': '0262 605 24 12',
    'email': 'zaferiakopoulos@gtu.edu.tr',
    'address': 'Gebze Technical University Computer Engineering Building Gebze - Kocaeli - Turkey',
    'zipCode': '41400',
    'office': 'A2 Block, 254'
}

contact2 = {
    'name': 'Gizem Süngü',
    'phone': '0262 605 24 27',
    'email': 'gizeumsungu@gtu.edu.tr',
    'address': 'Gebze Technical University Computer Engineering Building Gebze - Kocaeli - Turkey',
    'zipCode': '41400',
    'office': 'A2 Block, 234'
}

@app.route('/')
def home():
   return render_template('index.html', definition=static_definition, contact1=contact1, contact2=contact2)

app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.register_blueprint(data_app, url_prefix="/data")
app.register_blueprint(formatter_app, url_prefix="/formatter")