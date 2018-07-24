from flask import Flask,render_template,request,json

import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("selection.html")


@app.route("/create",methods= ["GET" , "POST"])
def create():
    if request.method == "POST" :
        return render_template("create.html")
    else:
        print("get")
        return render_template("saving.html")


@app.route("/saving",methods= ["GET" , "POST"])
def saving():
    if request.method == "POST" :
        data = {};

        data = request.form.get("jsonFile")

        print(data)

        return render_template("saving.html")
    else:
        print("get")
        return render_template("saving.html")



@app.route("/edit",methods= ["GET" , "POST"])
def edit():
    if request.method == "POST" :
        return  render_template("edit.html")
    else:
        return render_template("edit.html")


@app.route("/list",methods= ["GET" , "POST"])
def list():
    if request.method == "POST" :
        return  render_template("list.html")
    else:
        return render_template("list.html")




@app.route("/listed",methods= ["GET" , "POST"])
def listed():
    if request.method == "POST" :
        graph = request.form.get("username")
        repo = request.form.get("valueOfRepo")
        shaKey = request.form.get("valueOfSHAkey")

        print(graph)
        print(repo)
        print(shaKey)

        data = {
            "operate" : "list",
            "datatype" : graph,
            "repo" : repo,
            "sha" : shaKey,
        }

        header = {'content-type': "application/json"}

        req = requests.post('http://10.1.40.164:8080/',data=json.dumps(data),headers = header)

        print(req.status_code)
        print(req.json())


        return render_template("listed.html",req = req.json())
    else:
        print("get")
        return render_template("listed.html")

@app.route("/delete",methods= ["GET" , "POST"])
def delete():
    if request.method == "POST" :
        return  render_template("delete.html")
    else:
        return render_template("delete.html")


if __name__ == '__main__':
   app.run(debug = True)



