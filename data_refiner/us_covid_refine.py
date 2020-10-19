import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
baseurl = os.path.dirname(os.path.abspath(__file__))
import numpy as np
import pandas as pd
from utils.file_helper import FileReader

class USCovidRefine:

    reference_date_list = []
    totalcountconfirmed_list = []
    totalcountdeaths_list = []

    def __init__(self):
        print(f'basedir: {baseurl}')
        self.reader = FileReader()

    def process(self):
        data = self.get_file()
        unique_date = data['date'].unique()
        for date in unique_date:
            self.data_refine(data, date)
        # print(self.reference_date_list)
        # print(self.totalcountconfirmed_list)
        # print(self.totalcountdeaths_list)
        self.save_csv()

    def get_file(self):
        self.reader.context = os.path.join(baseurl, 'data')
        self.reader.fname = 'statewide_cases.csv'
        data = self.reader.csv_to_dframe()
        # print(data)
        return data
    
    def drop_feature(self, data, reference_date):
        is_date = data['date'] == reference_date
        rows_for_date = data[is_date]
        rows_for_date = rows_for_date.drop('newcountconfirmed', axis=1)
        rows_for_date = rows_for_date.drop('newcountdeaths', axis=1)
        rows_for_date = rows_for_date.drop('county', axis=1)
        return rows_for_date


    def data_refine(self, data, reference_date):

        rows_for_date = self.drop_feature(data, reference_date)

        totalcountconfirmed_df = rows_for_date['totalcountconfirmed']
        totalcountconfirmed = sum(totalcountconfirmed_df)

        totalcountdeaths_df = rows_for_date['totalcountdeaths']
        totalcountdeaths = sum(totalcountdeaths_df)

        self.reference_date_list.append(reference_date)
        self.totalcountconfirmed_list.append(totalcountconfirmed)
        self.totalcountdeaths_list.append(totalcountdeaths)

        # raw_data = {'col0': [1, 2, 3, 4],
        #     'col1': [10, 20, 30, 40],
        #     'col2': [100, 200, 300, 400]}

    def save_csv(self):

        refined_dict = {'data': self.reference_date_list,
                        'totalcountconfirmed': self.totalcountconfirmed_list,
                        'totalcountdeaths': self.totalcountdeaths_list
                        }
        refined_data = pd.DataFrame(refined_dict)
        print(refined_data)

        context = os.path.join(baseurl, 'refined_data')
        filename = os.path.join(context, 'saved_dtatewide_cases.csv')
        refined_data.to_csv(filename, index=False)

if __name__ == '__main__':
    ucr = USCovidRefine()
    ucr.process()
    