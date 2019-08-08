import os
import datetime as dt
import DataFrameLoader as dfLoader
import CleaningDF as cDF
import Plots as showPlots
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection, preprocessing, metrics
import lightgbm as lgb

"""
Created on Fri Jul 26 13:48:19 2019

@author: apozidis
"""


def clean_data(df, to_drop):
    print("Data cleaning...")
    df = cDF.drop_constant_columns(df, to_drop)
    df = cDF.filling_na_values(df)
    df = cDF.replace_huge_string(df)
    df = cDF.normalizing(df)
    return df


print("Started at : " + str(dt.datetime.now().time()))
if os.path.exists("DataSets/train_cleaned.csv"):
    print("Loading cleaned train dataset...")
    train_df = dfLoader.load_df("DataSets/train_cleaned.csv")

    print("Loading cleaned test dataset...")
    test_df = dfLoader.load_df("DataSets/test_cleaned.csv")
elif os.path.exists("DataSets/train_new.csv"):
    print("Loading new train dataset...")
    train_df = dfLoader.load_df("DataSets/train_new.csv")
    constants_columns = cDF.discovering_constant_columns(train_df)
    train_df = clean_data(train_df, constants_columns)
    train_df.to_csv("DataSets/train_cleaned.csv", index=False)

    print("Loading new test dataset...")
    test_df = dfLoader.load_df("DataSets/test_new.csv")
    test_df = clean_data(test_df, constants_columns)
    test_df.to_csv("DataSets/test_cleaned.csv", index=False)
else:
    print("Loading train dataset...")
    train_df = dfLoader.load_df_clean_json("DataSets/train.csv", 100000)
    train_df.to_csv("DataSets/train_new.csv", index=False)

    print("Loading test dataset...")
    test_df = dfLoader.load_df_clean_json("DataSets/test.csv", 100000)
    test_df.to_csv("DataSets/test_new.csv", index=False)

print("Finished at : " + str(dt.datetime.now().time()))

print('Train data shape : ' + str(train_df.shape))
print('Test data shape : ' + str(test_df.shape))

showPlots.show_revenue_graph(train_df)
showPlots.show_device_browser(train_df)
showPlots.show_cross_revenue_browser(train_df)
showPlots.show_channel_grouping(train_df)
showPlots.show_channel_cross_browsers(train_df)
showPlots.show_operating_systems(train_df)
showPlots.show_most_used_browser_by_os(train_df)
