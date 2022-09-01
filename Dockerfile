FROM python:3.9-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python app.py