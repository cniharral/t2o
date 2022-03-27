# syntax=docker/dockerfile:1
  
FROM python:3.8-slim-buster

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "blockchain.py/manage.py", "runserver", "0.0.0.0", "8888"]

