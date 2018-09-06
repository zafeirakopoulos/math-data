from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/software/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add Software Record**
    
    This function allows to add a software record.

    :param data: incoming json file.
    :type data:

    - input example:
        r = {
            "software": "polymake"
            "version": ""
        }
    :returns: SHA key of added software record.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/software/add/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            ...
        }'

    - Expected Success Response::

        HTTP Status Code: 201

        {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    - Expected Fail Response::

        HTTP Status Code: 400

        {'error': 'Duplicate software'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/software/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter Software Records **

    This function allows to retrieve filtered records matching with input dict data

    :param data: used to filter softwares
    :type data: String

    - input example:
        r = {
            ...
        }
    :returns: filtered software records list.
        return example:
            r = [
                { "software": "polymake"
                  "...": "..."
                },
                { "software": "latte"
                  "...": ""
                }
            ]

    - Example::
        curl -X POST https://10.1.18.42:8800/software/filter/ -H 'cache-control: no-cache' -H
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

@service.route('/software/get/<string:software_key>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Software Record **

    This function allows to fetch software record that match with input SHA key

    :param SHA: Key of requested software record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's software json record

        -return example:

            r = { "software": "polymake"
                  "...": "..."
                }

    - Example

        curl -X GET https://10.1.18.42:8800/software/get/<string:software_key>/ -H 'cache-control: no-cache' -H
        'content-type: application/json' \ -d
        '{
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }'

    - Expected Success Response::

        HTTP Status Code: 200

        {
            "software": "polymake"
            "version": ""
        }

    - Expected Fail Response::

        HTTP Status Code: 404

        {'error': 'Not found'}

    :exception:

"""
    response = {}
    return json.dumps(response)