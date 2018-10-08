#!/bin/sh
docker build -t mathdata --build-arg CACHEBUST=$(date +%s) .
docker run -it --restart unless-stopped mathdata
CONTAINER_ID=$(docker ps -alq)
docker cp $CONTAINER_ID:/doc_builder/doc/ .
docker stop $CONTAINER_ID