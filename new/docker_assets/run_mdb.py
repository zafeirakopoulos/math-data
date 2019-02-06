from gevent.pywsgi import WSGIServer
from mdb import app

http_server = WSGIServer(('', 5000), app)
print("About to start server")
http_server.serve_forever()
