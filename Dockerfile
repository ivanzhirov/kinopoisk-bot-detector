FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -yqq netcat

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./Pipfile ./Pipfile

RUN pipenv install --skip-lock --system --dev

COPY . .
