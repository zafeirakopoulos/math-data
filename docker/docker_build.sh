#!/bin/sh
docker build -t mathdata -f docker/Dockerfile --target documentation_builder .
docker run -it --restart unless-stopped mathdata
CONTAINER_ID=$(docker ps -alq)
# Get created build directory from container to local directory 
docker cp $CONTAINER_ID:/doc_builder/doc/ .
# stop container
docker stop $CONTAINER_ID