from flask import Flask, Blueprint, request, json, render_template
from md.views.home import home_app
from md.models import User
from md.core import create_response, serialize_list, logger

@home_app.route('/', methods=['GET'])
def index():
    static_definition = 'MathData is a system for efficient representation of mathematical data and benchmarking of mathematical software and algorithms. MathData is supported by the TUBITAK funded project 117E501 under the program 3501.'
    stats = ''

    return render_template('index.html',  definition=static_definition, stats=stats)

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
