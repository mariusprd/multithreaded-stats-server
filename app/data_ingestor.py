'''
    This module is responsible for reading the dataset and providing methods for statistics.
'''
import json
from threading import Event
import pandas as pd


class DataIngestor:
    '''
        This class is responsible for reading the dataset and providing methods
        to calculate statistics.
    '''
    def __init__(self, csv_path: str, data_loaded: Event = None):
        self.data_loaded = data_loaded

        # Read csv from csv_path
        self.data = pd.read_csv(csv_path)
        if self.data_loaded is not None:
            self.data_loaded.set()

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]


    def global_mean(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the average
            of the recorded values (Data_Value) from the total time interval (2011-2022)
            from the entire dataset.
        '''
        def inner_global_mean():
            res =  self.data[self.data['Question'] == question]['Data_Value'].mean()
            return json.dumps({"global_mean": res})

        return inner_global_mean


    def states_mean(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the average
            of the recorded values (Data_Value) from the total time interval (2011-2022)
            for each state, and sorts them in ascending order by mean.
        '''
        def inner_states_mean():
            ascending = question in self.questions_best_is_min
            res = (
                self.data[self.data['Question'] == question]
                .groupby('LocationDesc')['Data_Value']
                .mean()
                .sort_values(ascending=ascending)
            )
            return json.dumps(res.to_dict())

        return inner_states_mean


    def state_mean(self, question: str, state: str):
        '''
            Receives a question (from the set of questions above) and a state, and calculates
            the average of the recorded values (Data_Value) from the total time interval
            (2011-2022).
        '''
        def inner_state_mean():
            res = (
                self.data[
                    (self.data['Question'] == question) &
                    (self.data['LocationDesc'] == state)
                ]['Data_Value']
                .mean()
            )
            return json.dumps({state: res})

        return inner_state_mean


    def best5(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the average
            of the recorded values (Data_Value) from the total time interval (2011-2022)
            and returns the top 5 states.
        '''
        def inner_best5():
            ascending = question in self.questions_best_is_min
            res = (
                self.data[self.data['Question'] == question]
                .groupby('LocationDesc')['Data_Value']
                .mean()
                .sort_values(ascending=ascending)
                .head(5)
            )
            return json.dumps(res.to_dict())

        return inner_best5


    def worst5(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the average
            of the recorded values (Data_Value) from the total time interval (2011-2022)
            and returns the last 5 states.
        '''
        def inner_worst5():
            ascending = question in self.questions_best_is_max
            res = (
                self.data[self.data['Question'] == question]
                .groupby('LocationDesc')['Data_Value']
                .mean()
                .sort_values(ascending=ascending)
                .head(5)
            )
            return json.dumps(res.to_dict())

        return inner_worst5


    def diff_from_mean(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the difference
            between the global mean and the mean of each state.
        '''
        def inner_diff_from_mean():
            ascending = question in self.questions_best_is_min
            global_mean = self.data[self.data['Question'] == question]['Data_Value'].mean()
            states_mean =  (
                self.data[self.data['Question'] == question]
                .groupby('LocationDesc')['Data_Value']
                .mean()
                .sort_values(ascending=ascending)
            )
            res = global_mean - states_mean
            return json.dumps(res.to_dict())

        return inner_diff_from_mean


    def state_diff_from_mean(self, question: str, state: str):
        '''
            Receives a question (from the set of questions above) and a state, and calculates
            the difference between the global mean and the mean of the state.
        '''
        def inner_state_diff_from_mean():
            global_mean = self.data[self.data['Question'] == question]['Data_Value'].mean()
            state_mean = (
                self.data[
                    (self.data['Question'] == question) &
                    (self.data['LocationDesc'] == state)
                ]['Data_Value']
                .mean()
            )
            res = global_mean - state_mean
            return json.dumps({state: res})

        return inner_state_diff_from_mean


    def state_mean_by_category(self, question: str, state: str):
        '''
            Receives a question (from the set of questions above) and a state, and calculates
            the average value for each segment (Stratification1)
            from the categories (StratificationCategory1).
        '''
        def inner_state_mean_by_category():
            res = (
                self.data[
                    (self.data['Question'] == question) &
                    (self.data['LocationDesc'] == state)
                ].groupby(['StratificationCategory1', 'Stratification1'])
                ['Data_Value'].mean()
                .to_dict()
            )
            res = {str(k) : v for k, v in res.items()}
            return json.dumps({state: res})

        return inner_state_mean_by_category


    def mean_by_category(self, question: str):
        '''
            Receives a question (from the set of questions above) and calculates the average value
            for each segment (Stratification1) from the categories (StratificationCategory1)
            of each state.
        '''
        def inner_mean_by_category():
            res = (
                self.data[(self.data['Question'] == question)]
                .groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])
                ['Data_Value'].mean()
                .sort_index(level=0)
                .to_dict()
            )
            return json.dumps({str(tuple([k0, k1, k2])): v for (k0, k1, k2), v in res.items()})

        return inner_mean_by_category
