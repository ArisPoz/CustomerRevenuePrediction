import json
import pandas as pd
from pandas.io.json import json_normalize

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

"""
Created on Fri Jul 26 13:58:19 2019

@author: apozidis
"""


def load_df_clean_json(csv_path, chunk_size=50000):
    json_columns = ['device', 'geoNetwork', 'totals', 'trafficSource']
    chunk_list = []
    print("Loading csv data from " + csv_path + " to dataframe.")
    shape = 0
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size,
                             converters={column: json.loads for column in json_columns},
                             dtype={'fullVisitorId': 'str'}):
        shape += chunk.shape[0]
        print("Loaded : " + str(shape) + " lines.")
        chunk_list.append(chunk)

    print("Concat chunks in one dataframe.")
    df = pd.concat(chunk_list)
    print("Converting json columns to data frame columns.")
    for column in json_columns:
        print("Processing column : " + column)
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{sub_column}" for sub_column in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)

    return df


def load_df(csv_path, gui, chunk_size=50000):
    chunk_list = []
    print("Loading csv data from " + csv_path + " to dataframe.")
    shape = 0
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
        shape += chunk.shape[0]
        print("Loaded : " + str(shape) + " lines.")
        chunk_list.append(chunk)
        gui.update_progressbar(gui.get_progressbar_status() + 2)
    print("Concat chunks in one dataframe.")
    df = pd.concat(chunk_list)

    return df
