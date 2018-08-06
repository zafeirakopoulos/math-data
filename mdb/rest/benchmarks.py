from flask import Flask, Blueprint, request, json
import os
from mdb.data.db import DB
from mdb.data.io import *

benchmarks_app = Blueprint('benchmarks_app', __name__, template_folder='templates')

# @benchmarks_app.route('/', defaults={'page': 'index'})
# def index(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)

@benchmarks_app.route('/add_instance', methods=["POST"])
def add_instance():

    basedir = os.path.join(os.getcwd(), "data")
    global data
    data = DB(basedir)

    instance = request.json

    response = mdb.io.add_instance(data, instance)

    js = json.dumps(response)

    return js



@benchmarks_app.route('/shutdown', methods=["POST"])
def shutdown():
    flask.request.environ.get('werkzeug.server.shutdown')()
