from flask import Flask, Blueprint, request, json
from mdb.data.db import DB, Table
import os


service = Blueprint('service',__name__, template_folder='templates')

@service.route('/docker_registry/add',methods=["POST"])
def add(mdb: DB, data):
    """
    ** Add Docker Registry Record**

    This function allows to add a docker image

    :param data: docker image json file
    :type data:

    - input example:
        r = {

        }
    :returns: SHA key of added docker image.
        return example:
            r = {
                "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
            }

    - Example::
        curl -X POST https://10.1.18.42:8800/docker_registry/add/ -H 'cache-control: no-cache' -H
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

        {'error': 'Duplicate formatter'}

    :exception


    """

    SHA = "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
    return SHA

@service.route('/docker_registry/filter',methods=["POST"])
def filter(mdb: DB, data):
    """
    ** Filter Docker Image Records **

    This function allows to retrieve filtered records matching with input data

    :param data: Formatter to filter docker image records
    :type data:

    - input example:
        r = {
            ...
        }
    :returns: filtered docker image records list .
        return example:

            ...

    - Example::
        curl -X POST https://10.1.18.42:8800/docker_registry/filter/ -H 'cache-control: no-cache' -H
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

@service.route('/docker_registry/get/<string:format_SHA>',methods=["GET"])
def get(mdb: DB, SHA):
    """
    ** Get Docker Image Record **

    This function allows to fetch docker image record that match with input images SHA key

    :param SHA: Key of requested image record
    :type SHA: String

    - input example:
        r = {
            "sha": "18e8b2047eeefe9d45fa01a2f15b26bb62a3c471"
        }

    :returns: Given key's docker registry.

        -return example:

            ...

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