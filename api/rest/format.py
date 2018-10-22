from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/format/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add Formatter Record**

    This function allows to add a formatter

    :param data: format json file
    :type data:

    - input example:
        r = {
            "SHA_Formatter": "..."
            "from": "..."
            "to": "..."
            "Data_SHA": "..."
        }
    :returns: SHA key of added formatter.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/format/add/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "SHA_Formatter": "..."
            "from": "..."
            "to": "..."
            "Data_SHA": "..."
        }'

    - Expected Success Response::

        HTTP Status Code: 201

        {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    - Expected Fail Response::

        HTTP Status Code: 400

        {'error': 'Duplicate formatter'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/format/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter Formatter Records **

    This function allows to retrieve filtered records matching with input data

    :param data: Formatter to filter formatter records
    :type data:

    - input example:
        r = {
            ...
        }
    :returns: filtered formatter records list .
        return example(dict):
            r = [
                {
                    "SHA_Formatter": "..."
                    "from": "..."
                    "to": "..."
                    "Data_SHA": "..."
                },
                {  ... },
            ]

    - Example::
        curl -X POST https://10.1.18.42:8800/format/filter/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            ...
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

@service.route('/format/get/<string:format_SHA>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Formatter Record **

    This function allows to fetch format record that match with input SHA key

    :param SHA: Key of requested format record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's formatter.

        -return example:

            r = {
                    "SHA_Formatter": "..."
                    "from": "..."
                    "to": "..."
                    "Data_SHA": "..."
                }

    - Example

        curl -X GET https://10.1.18.42:8800/format/get/<string:format_SHA>/ -H 'cache-control: no-cache' -H
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