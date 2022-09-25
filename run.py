from app import MetricsFaker as App
from os import environ as env
import time

mongo_params = {
    "host":env.get('MONGO_HOST', "localhost"),
    "port": int(env.get('MONGO_PORT', 27017)),
    "db": env.get('MONGO_DB', 'mayaprotect')
}

faker_params = {
    "exporter_port": int(env.get('EXPORTER_PORT', 8000)),
    "min_owner": int(env.get('MIN_OWNER', 1)),
    "max_owner": int(env.get('MAX_OWNER', 2)),
    "min_stations_per_owner": int(env.get('MIN_STATIONS_PER_OWNER', 2)),
    "max_stations_per_owner": int(env.get('MAX_STATIONS_PER_OWNER', 5)),
    "min_hives_per_station": int(env.get('MIN_HIVES_PER_STATION', 8)),
    "max_hives_per_station": int(env.get('MAX_HIVES_PER_STATION', 25)),
}

app = App(mongo_params, faker_params, int(time.time() - 60 * 10))

if __name__ == '__main__':
    app.run()
