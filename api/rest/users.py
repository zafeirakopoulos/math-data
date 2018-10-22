from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/user/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add User Record**
    This function allows user to register and add user record to db.

    :param data: users information type in json dict
    :type data:

    - input example:
        r = {

            "name": ".."
            "account_type": "google"
            "account_name": ".."
        }
    :returns: SHA key of added user.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/user/add/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "name": "yunus emre avcı"
            "account_type": "google"
            "account_name": "ynsmravci@gmail.com"
        }'

    - Expected Success Response::

        HTTP Status Code: 201

        {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    - Expected Fail Response::

        HTTP Status Code: 400

        {'error': 'Duplicate user'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/user/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter User Records **

    This function allows to retrieve filtered records matching with input data

    :param data: requested json filter data
    :type data:

    - input example:
        r = {
            "user": "username"
        }
    :returns: All user list that has "username"
        return example:
            r = [
                {  "environment": "python2"},
                {  "environment": "python3"},
            ]

    - Example::
        curl -X POST https://10.1.18.42:8800/user/filter/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "environment": "python"
        }'

    - Expected Success Response::

        HTTP Status Code: 200

        [{
                "name": "yunus emre avcı"
                "account_type": "google"
                "account_name": "ynsmravci@gmail.com"
            },
            {
                "name": ".."
                "account_type": "gitlab"
                "account_name": "..

        }]

    - Expected Fail Response::

        HTTP Status Code: 404

        {'error': 'Not Found'}

    :exception


"""

    response = []

    return json.dumps(response)

@service.route('/user/get/<string:user_key>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Environment Record **

    This function allows to fetch user record that match with input SHA key

    :param SHA: Key of requested user record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's record

        -return example:

            r = {
                "name": "yunus emre avcı"
                "account_type": "google"
                "account_name": "ynsmravci@gmail.com"
            }

    - Example

        curl -X GET https://10.1.18.42:8800/user/get/<string:user_key>/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }'

    - Expected Success Response::

        HTTP Status Code: 200

        {
            ...
        }

    - Expected Fail Response::

        HTTP Status Code: 404

        {'error': 'Not found'}

    :exception:

"""
    response = {}
    return json.dumps(response)