import time
import unittest
import os
import docker
from app import MetricsFaker


class TestMetricsFaker(unittest.TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)

    def test_create_metrics_faker(self):
        self.assertTrue(type(self.__metrics_faker) == MetricsFaker)
    
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
