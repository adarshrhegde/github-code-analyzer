# Test Suite 

import unittest
from test_graph import TestGraph
from github_service_test import TestGithubService


test_classes_to_run = [TestGraph, TestGithubService, TestDiff]

loader = unittest.TestLoader()

suites_list = []
for test_class in test_classes_to_run:
    suite = loader.loadTestsFromTestCase(test_class)
    suites_list.append(suite)

big_suite = unittest.TestSuite(suites_list)

runner = unittest.TextTestRunner()
results = runner.run(big_suite)

#suite = unittest.TestLoader().loadTestsFromTestCase().loadTestsFromTestCase()
#unittest.TextTestRunner(verbosity=2).run(suite)