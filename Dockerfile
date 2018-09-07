 # Set base imamge
FROM ubuntu:18.04

# Identify the maintainer of an image
LABEL MAINTANER Zafeirakis Zafeirakopoulos
LABEL version = "0.1"
LABEL description = "Webapp Docker"

# copy project source to app directory
RUN mkdir /app
COPY . /app

# install python3 and its necessary plugins
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3-git
RUN apt-get install -y git

# upgrade pip and intall flask 
RUN python3.6 -m pip install pip --upgrade
RUN pip install flask

# change working directory
WORKDIR /app

# execute the web application
ENTRYPOINT ["python3","run-mdb.py"]

CMD ["postgres"]