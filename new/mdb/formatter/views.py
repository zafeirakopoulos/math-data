from flask import Flask, Blueprint, request, json, render_template
from mdb.formatter import formatter_app

@formatter_app.route('/formatter/<key>',methods=['GET', 'POST'])
def formatter(key):
    response = formatter_app.active_mdb.retrieve_formatter_from_database(key)
    return render_template("formatter.html",formatter=response)

@formatter_app.route('/formatters/<data_version>', methods=["GET"])
def formatters():
    return formatter_app.active_mdb.formatters_for(data_version)

@formatter_app.route('/format/<data>/<formatter>', methods=["GET"])
def format():
    return formatter_app.active_mdb.format()
