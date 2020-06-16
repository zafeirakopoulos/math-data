from flask import Flask, Blueprint
from flask_security import login_required
from md.backend import active_bench

benchmarks_app = Blueprint('benchmarks', __name__)
benchmarks_app.active_mdb = active_bench


import md.views.benchmarks.views
