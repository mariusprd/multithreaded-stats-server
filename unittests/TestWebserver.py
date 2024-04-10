'''
    This file is used to test the data statistics functions
'''
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.data_ingestor import DataIngestor

import unittest

# Initialize the data ingestor => This will load the data
data_ingestor = DataIngestor("unittests/input/test_input.csv")

# total score
total_score = 0
NUM_TESTS = 9

class TestDataIngestor(unittest.TestCase):
    '''
        This class contains the unit tests for the data statistics functions
    '''
    def generic_test(self, func: callable, ref_file: str) -> None:
        '''
            Generic test function
        '''
        global total_score
        res = func()
        # print(f"Test name: {func.__name__}")
        # print(res)
        # print("-------------------\n")
        with open(ref_file, "r", encoding="utf-8") as fin:
            ref_data = fin.read()

        self.assertEqual(res, ref_data)
        total_score += 1


    def test_global_mean(self):
        '''
            Test the global mean function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        self.generic_test(data_ingestor.global_mean(question=test_question), "unittests/ref/global_mean.json")


    def test_states_mean(self):
        '''
            Test the states mean function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        self.generic_test(data_ingestor.states_mean(question=test_question), "unittests/ref/states_mean.json")


    def test_state_mean(self):
        '''
            Test the state mean function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        test_state = "Alabama"
        self.generic_test(data_ingestor.state_mean(question=test_question, state=test_state), "unittests/ref/state_mean.json")


    def test_best5(self):
        '''
            Test the best5 function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        self.generic_test(data_ingestor.best5(question=test_question), "unittests/ref/best5.json")


    def test_worst5(self):
        '''
            Test the worst5 function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        self.generic_test(data_ingestor.worst5(question=test_question), "unittests/ref/worst5.json")


    def test_diff_from_mean(self):
        '''
            Test the diff_from_mean function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        self.generic_test(data_ingestor.diff_from_mean(question=test_question), "unittests/ref/diff_from_mean.json")


    def test_state_diff_from_mean(self):
        '''
            Test the state_diff_from_mean function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        test_state = "Alabama"
        self.generic_test(data_ingestor.state_diff_from_mean(question=test_question, state=test_state), "unittests/ref/state_diff_from_mean.json")


    def test_mean_by_category(self):
        '''
            Test the mean_by_category function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        test_state = "Alabama"
        self.generic_test(data_ingestor.state_mean_by_category(question=test_question, state=test_state), "unittests/ref/mean_by_category.json")


    def test_state_mean_by_category(self):
        '''
            Test the state_mean_by_category function
        '''
        test_question = "Percent of adults aged 18 years and older who have obesity"
        test_state = "Alabama"
        self.generic_test(data_ingestor.state_mean_by_category(question=test_question, state=test_state), "unittests/ref/state_mean_by_category.json")


if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    finally:
        print(f"Score: {total_score}/{NUM_TESTS}")