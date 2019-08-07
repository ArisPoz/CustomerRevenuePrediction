# -*- coding: utf-8 -*-
import os
import datetime as dt
import DataFrameLoader as dfLoader
import CleaningDF as cDF

"""
Created on Fri Jul 26 13:48:19 2019

@author: apozidis
"""


def clean_data(df):
    print("Data cleaning...")
    cDF.filling_na_values(df)
    constants = cDF.discovering_constant_columns(df)
    # cDF.show_data(train_df)
    # cDF.show_data(test_df)
    df = cDF.drop_constant_columns(df, constants)
    return df


print(dt.datetime.now())
if os.path.exists("DataSets/train_cleaned.csv"):
    print("Loading cleaned train dataset...")
    train_df = dfLoader.load_df("DataSets/train_cleaned.csv")
elif os.path.exists("DataSets/train_new.csv"):
    print("Loading new train dataset...")
    train_df = dfLoader.load_df("DataSets/train_new.csv")
    train_df = clean_data(train_df)
    train_df.to_csv("DataSets/train_cleaned.csv", index=False)
else:
    print("Loading train dataset...")
    train_df = dfLoader.load_df_clean_json("DataSets/train.csv", 100000)
    train_df.to_csv("DataSets/train_new.csv", index=False)

if os.path.exists("DataSets/test_cleaned.csv"):
    print("Loading cleaned test dataset...")
    test_df = dfLoader.load_df("DataSets/test_cleaned.csv")
elif os.path.exists("DataSets/test_new.csv"):
    print("Loading new test dataset...")
    test_df = dfLoader.load_df("DataSets/test_new.csv")
    test_df = clean_data(test_df)
    test_df.to_csv("DataSets/test_cleaned.csv", index=False)
else:
    print("Loading test dataset...")
    test_df = dfLoader.load_df_clean_json("DataSets/test.csv", 100000)
    test_df.to_csv("DataSets/test_new.csv", index=False)

print("Data loaded.")
print(dt.datetime.now())
print(train_df.columns)
print(test_df.columns)
