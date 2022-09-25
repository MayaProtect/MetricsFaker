import unittest
from tests import test_hive_event, test_hive_event_collection, test_hive, test_hive_collection
from tests import test_metrics_history, test_station, test_station_collection, test_owner
from tests import test_faker_hive, test_faker_station


def run_tests(verbosity: int = 2):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromModule(test_hive_event))
    suite.addTest(loader.loadTestsFromModule(test_hive_event_collection))
    suite.addTest(loader.loadTestsFromModule(test_hive))
    suite.addTest(loader.loadTestsFromModule(test_hive_collection))
    suite.addTest(loader.loadTestsFromModule(test_metrics_history))
    suite.addTest(loader.loadTestsFromModule(test_station))
    suite.addTest(loader.loadTestsFromModule(test_station_collection))
    suite.addTest(loader.loadTestsFromModule(test_owner))
    suite.addTest(loader.loadTestsFromModule(test_faker_hive))
    suite.addTest(loader.loadTestsFromModule(test_faker_station))
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite)


if __name__ == "__main__":
    run_tests(2)
