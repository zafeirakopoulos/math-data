# Set base image as debian
FROM debian:stable-slim as base

LABEL description = "MDB Container"

RUN apt-get update && apt-get install -yq --no-install-recommends \
	  apt-utils \
    wget \
    bash \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    build-essential \
    m4 \
    yasm \
    cmake \
    git

RUN apt-get update && apt-get install -yq --no-install-recommends \
   python3-pip \
   python3-venv \
   python3-git \
   python3-setuptools \
   python3-dev \
   python3-wheel




RUN pip3 install flask
RUN pip3 install request
RUN pip3 install jinja2
RUN pip3 install gevent
RUN pip3 install GitPython

RUN pip3 install  bootstrap-flask


COPY docker_assets/run_mdb.py /mathdata/run_mdb.py
COPY mdb /mathdata/mdb
COPY local /mathdata/local
COPY md_def.py /mathdata/md_def.py


WORKDIR /mathdata
ENTRYPOINT ["python3","run_mdb.py"]
