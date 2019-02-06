#!/bin/sh
docker build -t mathdata -f Dockerfile .
docker run --publish=8800:5000 mathdata
#--restart unless-stopped
CONTAINER_ID=$(docker ps -alq)
