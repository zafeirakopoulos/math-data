from flask import Flask, Blueprint, request, json, render_template, jsonify
from flask_login import current_user
from md.views.mdl import mdl_app
from werkzeug.utils import secure_filename
import os
import sys

import json as json_beautifier

##########################
##########################
##   API
##########################
##########################
@mdl_app.route('/api/validate/<instance_key>/<datastructure_key>',methods=['GET', 'POST'])
def validate_instance(instance_key,datastructure_key):
    return mdl_app.active_mdl.validate_instance(instance_key,datastructure_key)
