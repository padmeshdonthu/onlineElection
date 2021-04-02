FROM ubuntu:18.04

LABEL maintainer="Padmesh Donthu <pd616769@dal.ca>"

RUN apt-get update

RUN apt-get install -y python3 python3-dev python3-pip


COPY /requirements.txt /requirements.txt


WORKDIR /


RUN pip3 install -r requirements.txt


EXPOSE 5000
COPY . /


ENV FLASK_APP=online_election
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV FLASK_RUN_PORT=5000
CMD [ "flask", "run", "--host", "0.0.0.0" ]

