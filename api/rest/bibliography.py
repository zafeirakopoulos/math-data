from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/bib/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add Bibliographic Record**
    This function allows to add a bib data.

    :param data: incoming json file.
    :type data:

    - input example(dict:
        r = {
            ...
        }
    :returns: SHA key of added bib dictionary.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/bib/add/ -H 'cache-control: no-cache' -H
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

        {'error': '..'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/bib/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter Bib Data **

    This function allows to retrieve filtered records matching with input dict data

    :param data: Dictionary to filter bib records
    :type data: String

    - input example(dict):
        r = {
            ...
        }
    :returns: SHA key of added bib dictionary.
        return example(dict):
            r = [
                { ... },
                { ... },
            ]

    - Example::
        curl -X POST https://10.1.18.42:8800/bib/filter/ -H 'cache-control: no-cache' -H
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

        HTTP Status Code: 400

        {'error': '..'}

    :exception


"""

    response = []

    return json.dumps(response)

@service.route('/bib/get/<string:bibdata_key>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Bib Data **

    This function allows to fetch bib record that match with input SHA key

    :param SHA: Key of requested bib record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's record as json dictionary

        -return example:

            r = {
                ...
            }

    - Example

        curl -X GET https://10.1.18.42:8800/bib/get/<string:bibdata_key>/ -H 'cache-control: no-cache' -H
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