# Set base image as debian
FROM debian:stable-slim as base


LABEL description = "MD"

ENV BUILD_OUT =/output
ENV JINJA_VERSION=2.10
ENV REQUESTS=2.19.1

FROM base AS essential_builder

RUN apt-get update && apt-get install -yq --no-install-recommends \
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
   python3-dev\
   python3-git \
   python3-venv


RUN export LIB_PATH=$LIB_PATH:$BUILD_OUT

FROM essential_builder AS documentation_builder

WORKDIR doc_build

RUN pip3 install python-sphinx
RUN pip3 install rinohtype

FROM essential_builder AS service_builder

WORKDIR service_build

RUN pip3 install flask
RUN pip3 install request