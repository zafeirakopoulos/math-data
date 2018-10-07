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
# RUN apt-get update && apt-get install -yq --no-install-recommends python-sphinx
RUN pip3 install alabaster \
	Babel==2.6.0 \
	certifi==2018.4.16 \
	chardet==3.0.4 \
	click==6.7 \
	CommonMark==0.5.4 \
	docutils==0.14 \
	idna==2.7 \
	imagesize==1.0.0 \
	itsdangerous==0.24 \
	MarkupSafe==1.0 \
	packaging==17.1 \
	purepng==0.2.0 \
	Pygments==2.2.0 \
	pyparsing==2.2.0 \
	pytz==2018.4 \
	recommonmark==0.4.0 \
	rinohtype \
	six==1.11.0 \
	snowballstemmer==1.2.1 \
	Sphinx==1.4.8 \
	sphinxcontrib-websupport==1.1.0 \
	SQLAlchemy==1.2.8 \
	urllib3==1.23 \
	Werkzeug==0.14.1

ARG CACHEBUST=1

RUN mkdir /doc_builder
# copy necessary files for documentation
COPY . /doc_builder

WORKDIR doc_builder

RUN chmod +x makedoc.sh

ENTRYPOINT ["./makedoc.sh"]

FROM essential_builder AS service_builder

RUN mkdir /service_build
COPY . /service_build
WORKDIR service_build

ENTRYPOINT ["./start_mdb.sh"]