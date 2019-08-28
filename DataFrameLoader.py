import json
import pandas as pd
from pandas.io.json import json_normalize
import CleaningDF as cDF
import os

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

"""
Created on Fri Jul 26 13:58:19 2019

@author: apozidis
"""


def convert_json_columns_and_load(csv_path, gui, chunk_size=50000):
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
        gui.update_progressbar(gui.get_progressbar_status() + 1)

    print("Concat chunks in one dataframe.")
    df = pd.concat(chunk_list)
    print("Converting json columns to data frame columns.")
    for column in json_columns:
        print("Processing column : " + column)
        column_as_df = json_normalize(df[column])
        column_as_df.columns = [f"{column}.{sub_column}" for sub_column in column_as_df.columns]
        df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
        gui.update_progressbar(gui.get_progressbar_status() + 1)

    return df


def load_df(csv_path, gui, chunk_size=150000):
    chunk_list = []
    print("Loading csv data from " + csv_path + " to dataframe.")
    shape = 0
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False,
                             dtype={'fullVisitorId': 'str'}):
        shape += chunk.shape[0]
        print("Loaded : " + str(shape) + " lines.")
        chunk_list.append(chunk)
        if 'train' in csv_path:
            gui.update_progressbar(gui.get_progressbar_status() + 7.5)
        else:
            gui.update_progressbar(gui.get_progressbar_status() + 25)
    print("Concat chunks in one dataframe.")
    df = pd.concat(chunk_list)

    return df


def load_train_set(ui):
    ui.update_progressbar(0)
    global constants_columns
    if os.path.exists("DataSets/train_cleaned.csv"):
        ui.console_output.append("Loading cleaned train dataset...")
        train_df = load_df("DataSets/train_cleaned.csv", ui)
    else:
        ui.console_output.append("Loading train dataset...")
        train_df = convert_json_columns_and_load("DataSets/train.csv", ui)
        constants_columns = cDF.discovering_constant_columns(train_df)
        train_df = clean_data(train_df, constants_columns, ui)
        train_df.to_csv("DataSets/train_cleaned.csv", index=False)
    return train_df


def load_test_set(ui):
    ui.update_progressbar(0)
    if os.path.exists("DataSets/test_cleaned.csv"):
        ui.console_output.append("Loading cleaned test dataset...")
        test_df = load_df("DataSets/test_cleaned.csv", ui)
    else:
        ui.console_output.append("Loading test dataset...")
        test_df = convert_json_columns_and_load("DataSets/test.csv", ui)
        test_df = clean_data(test_df, constants_columns, ui)
        test_df.to_csv("DataSets/test_cleaned.csv", index=False)
    return test_df


def clean_data(df, to_drop, ui):
    print("Data cleaning...")
    ui.console_output.append("Dropping Constant Columns...")
    df = cDF.drop_constant_columns(df, to_drop)
    ui.console_output.append("Replacing Huge String with Primitives...")
    df = cDF.replace_huge_string(df)
    ui.console_output.append("Filling NA Values...")
    df = cDF.filling_na_values(df)
    ui.console_output.append("Normalizing...")
    df = cDF.normalizing(df)
    ui.console_output.append("Processing Date From Linux Time --> Day/Week/Month/Year...")
    df = cDF.add_date_features(df)
    ui.console_output.append("Fixing Date Format...")
    df = cDF.date_process(df)
    return df
