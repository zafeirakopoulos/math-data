import mdb
from mdb.rest import app
from mdb.data.setup import *
import http.server
import socketserver
import sys

data_path = sys.argv[1]
# bench_path = sys.argv[2]

print(mdb.data.setup.__mdb)

mdb.data.setup.__mdb = MDB(data_path)
# bench = Bench(bench_path)

PORT = 8088
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

app.run()
