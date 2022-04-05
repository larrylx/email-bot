# v0.0.1
FROM python:3.9

RUN mkdir /app/
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY /app /app

CMD gunicorn -b 0.0.0.0:5000 app:app