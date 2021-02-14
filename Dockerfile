FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip

COPY ./src/ ./src
WORKDIR ./src

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 app.py