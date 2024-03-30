'''
    This file contains the unit tests for the webserver
'''
from datetime import datetime
from time import sleep
import json
import unittest
import os
import requests
from deepdiff import DeepDiff

class TestWebserver(unittest.TestCase):
    '''
        This class contains the unit tests for the webserver
    '''
    total_score = 0
    NUM_TESTS = 5


    def setUp(self):
        os.system("rm -rf results/*")


    def get_request(self, url: str):
        '''
            Sends a GET request to the webserver
        '''
        return requests.get(f"http://127.0.0.1:5000{url}")


    def post_request(self, url: str, input_path: str):
        '''
            Sends a POST request to the webserver
        '''
        with open(input_path, "r", encoding="utf-8") as fin:
            req_data = json.load(fin)

        return requests.post(f"http://127.0.0.1:5000{url}", json=req_data)


    def check_res_timeout(self, res_callable, ref_result, timeout_sec = 1, poll_interval = 0.2):
        '''
            Checks the response of a job until it is done or the timeout is reached
            This function is copy pasted from checker.py
        '''
        initial_timestamp = datetime.now()
        while True:
            response = res_callable()
            # print(response)

            # Asserting that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Asserting the response data
            response_data = response.json()
            # print(f"Response_data\n{response_data}")
            if response_data['status'] == 'done':
                # print(f"Response data {response_data['data']} and type {type(response_data['data'])}")
                # print(f"Ref data {ref_result} and type {type(ref_result)}")
                d = DeepDiff(response_data['data'], ref_result, math_epsilon=0.01)
                self.assertTrue(d == {}, str(d))
                break

            if response_data['status'] == 'running':
                current_timestamp = datetime.now()
                time_delta = current_timestamp - initial_timestamp
                if time_delta.seconds > timeout_sec:
                    self.fail("Operation timedout")
                else:
                    sleep(poll_interval)


    def test_global_mean(self):
        '''
            Tests the global_mean endpoint
        '''
        res = self.post_request("/api/global_mean", "tests/global_mean/input/in-1.json")
        job_id = res.json()["job_id"]

        with open("tests/global_mean/output/out-1.json", "r", encoding="utf-8") as f:
            ref_res = json.load(f)

        self.check_res_timeout(lambda: self.get_request(f"/api/get_results/{job_id}"), ref_res)
        TestWebserver.total_score += 1


    def test_jobs(self):
        '''
            Tests the jobs endpoint
        '''
        res = self.get_request("/api/jobs")
        self.assertEqual(res.status_code, 200)

        # open the unittests/output/ file and check the response
        with open("unittests/output/jobs_after__global_mean.json", "r", encoding="utf-8") as f:
            ref_res = json.load(f)
        res = res.json()
        d = DeepDiff(res, ref_res, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
        TestWebserver.total_score += 1


    def test_num_jobs(self):
        '''
            Tests the num_jobs endpoint
        '''
        res = self.get_request("/api/num_jobs")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["num_jobs"], 0)
        TestWebserver.total_score += 1


    def test_shutdown(self):
        '''
            Tests the shutdown endpoint
        '''
        res = self.get_request("/api/graceful_shutdown")
        self.assertEqual(res.status_code, 200)
        TestWebserver.total_score += 1


    def test_after_shutdown(self):
        '''
            Tests the jobs endpoint after shutdown
        '''
        # check if the a task can be added after shutdown
        res = self.post_request("/api/global_mean", "tests/global_mean/input/in-1.json")
        self.assertEqual(res.status_code, 200)
        status = res.json()["status"]
        self.assertEqual(status, "error")
        TestWebserver.total_score += 1


    @staticmethod
    def suite():
        '''
            Returns the test suite for this module
        '''
        suite = unittest.TestSuite()
        suite.addTest(TestWebserver("test_global_mean"))
        suite.addTest(TestWebserver("test_jobs"))
        suite.addTest(TestWebserver("test_num_jobs"))
        suite.addTest(TestWebserver("test_shutdown"))
        suite.addTest(TestWebserver("test_after_shutdown"))
        return suite


if __name__ == '__main__':
    try:
        runner = unittest.TextTestRunner()
        runner.run(TestWebserver.suite())
    finally:
        print(f"TOTAL SCORE: {TestWebserver.total_score}/{TestWebserver.NUM_TESTS}")
