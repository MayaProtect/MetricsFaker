FROM python:3.10-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV MONGO_HOST=mongodb
ENV MONGO_PORT=27017
ENV MONGO_DB=mayaprotect
ENV MIN_OWNER=2
ENV MAX_OWNER=25
ENV MIN_STATIONS_PER_OWNER=1
ENV MAX_STATIONS_PER_OWNER=10
ENV MIN_HIVES_PER_STATION=5
ENV MAX_HIVES_PER_STATION=20

EXPOSE 8000

CMD python run.py
