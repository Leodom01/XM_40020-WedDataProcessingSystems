FROM ubuntu:latest

RUN apt update

RUN apt install -y python3

RUN apt install -y python3-pip

RUN pip install -U pip setuptools wheel

RUN pip install -U spacy

RUN python3 -m spacy download en_core_web_sm

RUN pip install nltk

RUN pip install beautifulsoup4
