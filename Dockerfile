# Set base image as debian
FROM debian:stable-slim as base

VOLUME ["/mdb_vol"]

LABEL description = "MDB Container"

# General Variables
ENV DEBIAN_FRONTEND noninteractive


FROM base AS essential_builder

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

FROM essential_builder AS documentation_builder

RUN mkdir /doc_build
COPY . /doc_build
WORKDIR doc_build

RUN apt-get install -yq --no-install-recommends python-sphinx

RUN pip3 install rinohtype

ENTRYPOINT ["./makedoc.sh"]

CMD ["postgres"]

FROM essential_builder AS service_builder

RUN mkdir /service_build
COPY . /service_build
WORKDIR service_build

RUN pip3 install flask
RUN pip3 install request
RUN pip3 install jinja2

ENTRYPOINT ["./start_mdb.sh"]

CMD ["postgres"]