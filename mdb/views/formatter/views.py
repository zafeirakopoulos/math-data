from flask import Flask, Blueprint, request, json, render_template
from mdb.views.formatter import formatter_app

@formatter_app.route('/formatter/',methods=['GET', 'POST'])
def formatter():
    #response = formatter_app.active_mdb.retrieve_formatter_from_database(key)
    return render_template("formatter/formatter.html",formatter=response)

@formatter_app.route('/formatters/', methods=["GET"])
def formatters():

    #response = formatter_app.active_mdb.formatters_for()
    return render_template("formatter/formatters.html")

@formatter_app.route('/format/<data>/<formatter>', methods=["GET"])
def format():
    return formatter_app.active_mdb.format()
