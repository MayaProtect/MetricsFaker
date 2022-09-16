from app import MetricsFaker as App
from os import environ as env
import time

mongo_params = {
    "host": 'mongodb' if env.get('MONGO_HOST') is None else env.get('MONGO_HOST'),
    "port": 27017 if env.get('MONGO_PORT') is None else env.get('MONGO_PORT'),
    "db": 'metrics_faker' if env.get('MONGO_DB') is None else env.get('MONGO_DB')
}

faker_params = {
    "exporter_port": 8000 if env.get('EXPORTER_PORT') is None else env.get('EXPORTER_PORT'),
    "min_owner": 1 if int(env.get('MIN_OWNER')) is None else int(env.get('MIN_OWNER')),
    "max_owner": 2 if int(env.get('MAX_OWNER')) is None else int(env.get('MAX_OWNER')),
    "min_stations_per_owner": 2 if int(env.get('MIN_STATIONS_PER_OWNER')) is None else int(env.get('MIN_STATIONS_PER_OWNER')),
    "max_stations_per_owner": 5 if int(env.get('MAX_STATIONS_PER_OWNER')) is None else int(env.get('MAX_STATIONS_PER_OWNER')),
    "min_hives_per_station": 8 if int(env.get('MIN_HIVES_PER_STATION')) is None else int(env.get('MIN_HIVES_PER_STATION')),
    "max_hives_per_station": 25 if int(env.get('MAX_HIVES_PER_STATION')) is None else int(env.get('MAX_HIVES_PER_STATION')),
}

app = App(mongo_params, faker_params, int(time.time() - 60 * 10))

if __name__ == '__main__':
    app.run()
