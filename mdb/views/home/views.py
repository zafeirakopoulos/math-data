from flask import Flask, Blueprint, request, json, render_template
from mdb.views.home import home_app
from mdb.models import User
from mdb.core import create_response, serialize_list, logger

@home_app.route('/', methods=['GET'])
def index():
    static_definition = '"MathData - A system for efficient representation of mathematical data and benchmarking of mathematical software and algorithms" is a TUBITAK funded project aiming to create a standard for representing mathematical data and testing mathematical software.\nThe duration of the project is 18 months and it started on October 2017.'
    stats = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

    return render_template('index.html', definition=static_definition, stats=stats)

@home_app.route('/contact', methods=['GET'])
def contact():
    contact1 = {
        'name': 'Dr. Zafeirakis Zafeirakopoulos',
        'phone': '0262 605 24 12',
        'email': 'zafeirakopoulos@gtu.edu.tr'
    }

    contact2 = {
        'name': 'Gizem Süngü',
        'phone': '0262 605 24 27',
        'email': 'gizeumsungu@gtu.edu.tr'
    }

    contact3 = {
        'name': 'Elif Armağan',
        'email': 'esarmagan@gtu.edu.tr'
    }

    return render_template('contact.html', contact1=contact1, contact2=contact2, contact3=contact3)

# function that is called when you visit /persons
@home_app.route("/persons", methods=["GET"])
def get_persons():
    persons = User.query.all()
    return create_response(data={"persons": serialize_list(persons)})


@home_app.route('/documentation', methods=['GET'])
def documentation():

    return render_template('documentation.html')
