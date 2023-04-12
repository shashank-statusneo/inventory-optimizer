# syntax=docker/dockerfile:1

FROM python:3.10-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY login/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]
