from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/environment/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add Environment Record**
    This function allows to add an environment data.

    :param data: environment type
    :type data: string

    - input example:
        r = {
            "environment": "python3"
        }
    :returns: SHA key of added environment.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/environment/add/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "environment": "python3"
        }'

    - Expected Success Response::

        HTTP Status Code: 201

        {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    - Expected Fail Response::

        HTTP Status Code: 400

        {'error': 'Duplicate environment'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/environment/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter Environment Records **

    This function allows to retrieve filtered records matching with input data

    :param data: Environment type to filter environment records
    :type data: String

    - input example:
        r = {
            "environment": "python"
        }
    :returns: filtered environment records list .
        return example(dict):
            r = [
                {  "environment": "python2"},
                {  "environment": "python3"},
            ]

    - Example::
        curl -X POST https://10.1.18.42:8800/environment/filter/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "environment": "python"
        }'

    - Expected Success Response::

        HTTP Status Code: 200

        {
            ...
        }

    - Expected Fail Response::

        HTTP Status Code: 404

        {'error': 'Not Found'}

    :exception


"""

    response = []

    return json.dumps(response)

@service.route('/environment/get/<string:envdata_key>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Environment Record **

    This function allows to fetch environment record that match with input SHA key

    :param SHA: Key of requested environment record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's environment.

        -return example:

            r = {
                "environment": "python3"
            }

    - Example

        curl -X GET https://10.1.18.42:8800/environment/get/<string:envdata_key>/ -H 'cache-control: no-cache' -H
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