import os
import json
import pandas as pd
from threading import Event


class DataIngestor:
    def __init__(self, csv_path: str, data_loaded: Event):
        self.data_loaded = data_loaded

        # Read csv from csv_path
        self.data = pd.read_csv(csv_path)
        print(f"Finished reading data")
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

    def states_mean(self, question: str):
        def inner():
            ascending = question in self.questions_best_is_min
            return self.data[self.data['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=ascending).to_json()
        
        return inner
