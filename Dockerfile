FROM python:3.10
EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip -r requirements.txt

COPY run.py /
CMD python run.py