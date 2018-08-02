from flask import Flask,render_template,request, jsonify
from database import manage,io
import os
app = Flask(__name__)


jsonType = {

    "raw": {"dense": {"structure": "matrix"},
            "sparse": {"structure": "list"}
            },

    "typeset": {},

    "features": {"directed": {"structure": "boolean"}
                     }
}

r = {
        "raw": "something-",
        "features": "something-",
        "semantics": "something-",
        "context":  {"edge": {"1": 99, "2": 3},
                     "vertex": [{"first": 1, "second": 2},
                                {"first": 2, "second": 3}]},
        "typeset": "something-",
        "commit": "commit-message"
    }
@app.route("/",methods= ["GET" , "POST"])
def start():
    if request.method == "POST":
        basedir = os.path.join(os.getcwd(), "data")
        data = manage.mdb(basedir=basedir)
        print(io.add_instance(data,r))
    return render_template("mathData.html")



@app.route('/datatypes',methods= ["GET" , "POST"])
def get_products():

    data1 = request.form.get("jsonFile")
    print("form", *request.form.items())
    print(data1)

    return jsonify({'jsonType': jsonType})


if __name__ == '__main__':
   app.run(debug = True)



