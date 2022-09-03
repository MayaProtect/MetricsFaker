import unittest
from tests import *


def run_tests(verbosity: int = 3):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromModule(test_hive_event))
    suite.addTest(loader.loadTestsFromModule(test_hive_event_collection))
    suite.addTest(loader.loadTestsFromModule(test_hive))
    suite.addTest(loader.loadTestsFromModule(test_hive_collection))
    suite.addTest(loader.loadTestsFromModule(test_metrics_history))
    suite.addTest(loader.loadTestsFromModule(test_station))
    suite.addTest(loader.loadTestsFromModule(test_station_collection))
    # suite.addTest(loader.loadTestsFromModule(test_monitored_object))
    # suite.addTest(loader.loadTestsFromModule(test_faker))
    suite.addTest(loader.loadTestsFromModule(test_owner))
    suite.addTest(loader.loadTestsFromModule(test_faker_hive))
    suite.addTest(loader.loadTestsFromModule(test_faker_station))
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite)


if __name__ == "__main__":
    run_tests(2)
