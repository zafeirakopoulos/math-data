from flask import Flask, Blueprint, request, json, render_template, jsonify
from flask_login import current_user
from md.views.benchmarks import benchmarks_app
from md.core import logger
from werkzeug.utils import secure_filename
import os
import sys

import json as json_beautifier

##########################
##########################
##   API
##########################
##########################


##########################
##########################
##   HTML
##########################
##########################
@benchmarks_app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("benchmarks/index.html")


@benchmarks_app.route('/benchmarks', methods=['GET', 'POST'])
def benchmarks():
    return render_template("benchmarks/benchmarks.html")


@benchmarks_app.route('/software', methods=['GET', 'POST'])
def software():
    return render_template("benchmarks/software.html")


@benchmarks_app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template("benchmarks/create.html")


@benchmarks_app.route('/create_benchmark', methods=['GET', 'POST'])
def create_benchmark():
    return render_template("benchmarks/create_benchmark.html")


@benchmarks_app.route('/create_software', methods=['GET', 'POST'])
def create_software():
    return render_template("benchmarks/create_software.html")



# function to get change list
@benchmarks_app.route('/editor', methods=["GET", "POST"])
def editor_page():
    return render_template("benchmarks/editor.html")
