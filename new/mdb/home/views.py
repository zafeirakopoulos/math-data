from flask import Flask, Blueprint, request, json, render_template
from mdb.home import home_app

@home_app.route('/', methods=['GET'])
def index():
    static_definition = '"MathData - A system for efficient representation of mathematical data and benchmarking of mathematical software and algorithms" is a TUBITAK funded project aiming to create a standard for representing mathematical data and testing mathematical software.\nThe duration of the project is 18 months and it started on October 2017.'
    stats = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
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

    return render_template('index.html', definition=static_definition, stats=stats, contact1=contact1, contact2=contact2)