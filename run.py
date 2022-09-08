from app import MetricsFaker as App
from os import environ as env
import time

mongo_params = {
    "host": 'localhost' if env.get('MONGO_HOST') is None else env.get('MONGO_HOST'),
    "port": 27017 if env.get('MONGO_PORT') is None else env.get('MONGO_PORT'),
}

opentsdb_params = {
    "host": 'localhost' if env.get('OPENTSDB_HOST') is None else env.get('OPENTSDB_HOST'),
    "port": 4242 if env.get('OPENTSDB_PORT') is None else env.get('OPENTSDB_PORT'),
}

faker_params = {
    "min_owner": 1 if env.get('MIN_OWNER') is None else env.get('MIN_OWNER'),
    "max_owner": 2 if env.get('MAX_OWNER') is None else env.get('MAX_OWNER'),
    "min_stations_per_owner": 2 if env.get('MIN_STATIONS_PER_OWNER') is None else env.get('MIN_STATIONS_PER_OWNER'),
    "max_stations_per_owner": 5 if env.get('MAX_STATIONS_PER_OWNER') is None else env.get('MAX_STATIONS_PER_OWNER'),
    "min_hives_per_station": 8 if env.get('MIN_HIVES_PER_STATION') is None else env.get('MIN_HIVES_PER_STATION'),
    "max_hives_per_station": 25 if env.get('MAX_HIVES_PER_STATION') is None else env.get('MAX_HIVES_PER_STATION'),
}

app = App(mongo_params, opentsdb_params, faker_params, int(time.time() - 60 * 10))

if __name__ == '__main__':
    app.run()
