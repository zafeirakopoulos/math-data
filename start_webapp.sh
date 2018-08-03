cd webapp
if ! type "python3" > /dev/null; then
    python -m SimpleHTTPServer
else
    python3 -m http.server
fi
cd ..
