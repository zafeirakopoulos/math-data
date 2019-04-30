FROM python:3.7
LABEL description = "MDB Container"

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -yq --no-install-recommends \
    apt-utils gcc wget bash bzip2 ca-certificates \
    sudo m4 yasm cmake git postgresql postgresql-contrib

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

# for the flask config
ENV FLASK_ENV=docker

RUN chmod +x docker_script.sh

EXPOSE 5000
#ENTRYPOINT [ "python", "manage.py", "runserver" ]
#ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "INFO", "manage:app" ]