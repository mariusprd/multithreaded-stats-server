import os
import json
import pandas as pd
from threading import Event


class DataIngestor:
    def __init__(self, csv_path: str, data_loaded: Event):
        self.data_loaded = data_loaded

        # Read csv from csv_path
        self.data = pd.read_csv(csv_path)
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


    def global_mean(self, question: str) -> str:
        def inner():
            res =  self.data[self.data['Question'] == question]['Data_Value'].mean()
            return json.dumps({"global_mean": res})
        
        return inner
        

    def states_mean(self, question: str) -> str:
        def inner():
            ascending = question in self.questions_best_is_min
            res =  self.data[self.data['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=ascending)
            return json.dumps(res.to_dict())
        
        return inner
    

    def state_mean(self, question: str, state: str) -> str:
        def inner():
            res = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]['Data_Value'].mean()
            return json.dumps({state: res})
        
        return inner
    

    def best5(self, question: str) -> str:
        def inner():
            ascending = question in self.questions_best_is_min
            res = self.data[self.data['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=ascending).head(5)
            return json.dumps(res.to_dict())
        
        return inner
    

    def worst5(self, question: str) -> str:
        def inner():
            ascending = question in self.questions_best_is_min
            res = self.data[self.data['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=not ascending).head(5)
            return json.dumps(res.to_dict())
        
        return inner
    

    def diff_from_mean(self, question: str) -> str:
        def inner():
            ascending = question in self.questions_best_is_min
            global_mean = self.data[self.data['Question'] == question]['Data_Value'].mean()
            states_mean =  self.data[self.data['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=ascending)
            res = global_mean - states_mean
            return json.dumps(res.to_dict())
            
        return inner
    

    def state_diff_from_mean(self, question: str, state: str) -> str:
        def inner():
            global_mean = self.data[self.data['Question'] == question]['Data_Value'].mean()
            state_mean = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]['Data_Value'].mean()
            res = global_mean - state_mean
            return json.dumps({state: res})
        
        return inner


    def state_mean_by_category(self, question: str, state: str) -> str:
        def inner():
            data_for_state = self.data[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
            res = data_for_state.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean().to_dict()
            return json.dumps({state: json.dumps({str(tuple([k1, k2])): v for (k1, k2), v in res.items()})})

        return inner


    def mean_by_category(self, question: str) -> str:
        def inner():
            data_for_state = self.data[(self.data['Question'] == question)]
            res = data_for_state.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean().sort_index(level=0).to_dict()
            return json.dumps({str(tuple([k0, k1, k2])): v for (k0, k1, k2), v in res.items()})
        
        return inner
    
