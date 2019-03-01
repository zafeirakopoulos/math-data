#!/bin/sh
docker build -t mathdata -f Dockerfile .
docker run --publish=8800:5000 -d -v $(pwd)/mdb:/mathdata/mdb mathdata
#--restart unless-stopped
CONTAINER_ID=$(docker ps -alq)
