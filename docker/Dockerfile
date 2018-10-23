# Set base image as debian
FROM debian:stable-slim as base

LABEL description = "MDB Container"

ENV BUILT_ARTIFACTS=/output

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
   

RUN pip3 install flask
RUN pip3 install request
RUN pip3 install jinja2


FROM essential_builder AS documentation_builder

RUN pip3 install --upgrade setuptools
RUN apt-get install -yq --no-install-recommends \
	texlive-latex-recommended \
	texlive-latex-extra \
	texlive-fonts-recommended \
	latexmk \
	rst2pdf
RUN pip3 install Sphinx
	

RUN mkdir /doc_builder
# copy necessary files for documentation
COPY mdb /doc_builder/mdb
COPY mdl /doc_builder/mdl
COPY doc /doc_builder/doc
WORKDIR doc_builder
RUN chmod +x doc/makedoc.sh

ENTRYPOINT ["./doc/makedoc.sh"]

FROM essential_builder AS service_builder

RUN mkdir /service_build
COPY . /service_build
WORKDIR service_build

ENTRYPOINT ["./start_mdb.sh"]