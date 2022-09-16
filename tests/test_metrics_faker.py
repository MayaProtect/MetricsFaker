import time
import unittest
import os
import docker
from app import MetricsFaker


class TestMetricsFaker(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.__mongo_params = {
            "host": 'mongodb_mf_test',
            "port": 27019,
            "db": "mayaprotect"
        }

        self.__faker_params = {
            "min_owner": 10,
            "max_owner": 25,
            "min_stations_per_owner": 2,
            "max_stations_per_owner": 5,
            "min_hives_per_station": 8,
            "max_hives_per_station": 25,
        }

    def test_create_metrics_faker(self):
        self.assertTrue(type(self.__metrics_faker) == MetricsFaker)

    def test_run(self):
        pass
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("metrics_faker.log")
        print("File metrics_faker.log removed")
        docker_client = docker.from_env()
        docker_client.containers.get("mongodb_mf_test").remove(force=True)
        docker_client.close()

    @classmethod
    def setUpClass(cls) -> None:
        docker_client = docker.from_env()
        print("Starting mongo")
        docker_client.containers.run("mongo:4.2.3", detach=True, ports={'27017/tcp': 27019}, name="mongodb_mf_test")
        time.sleep(5)
        docker_client.close()
        print("Mongo started")
