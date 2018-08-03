cd mdb/services
export FLASK_APP=app.py
if ! type "python3" > /dev/null; then
    python -m flask run
else
    python3 -m flask run
fi
cd ..
