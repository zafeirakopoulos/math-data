# Restful API for MDB
I'm trying to extract API from core project. I'm trying to follow this folder structure: http://flask.pocoo.org/docs/1.0/patterns/packages/ with virtual environment. Similar project structure can be found in https://github.com/pallets/flask/tree/1.0.2/examples/tutorial

## Installing
From api folder

Create venv: 
```
python -m venv venv
```

Activate:
```bash
# on linux
. venv/bin/activate

# on Windows
venv\Scripts\activate.bat
```

Install current folder and its dependencies:
```
pip install -e .
```

## Run

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Accessing Endpoints
Open this address on your browser to access flask app: http://localhost:5000/. In `__init__.py` file there are definitions for Blueprints. Append their url_prefix and endpoints to access them. For example: http://localhost:5000/data/datatypes maps to `data.py` files `datatypes` endpoint.