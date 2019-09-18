import pandas as pd
import numpy as np
from datetime import datetime

"""
Created on Sat Jul 27 17:28:02 2019

@author: apozidis
"""


def filling_na_values(df):  # fillna numeric feature
    df['totals.pageviews'].fillna(1, inplace=True) # filling NA's with 1
    df['totals.newVisits'].fillna(0, inplace=True)  # filling NA's with 0
    df['totals.bounces'].fillna(0, inplace=True)  # filling NA's with 0
    df['trafficSource.isTrueDirect'].fillna(False, inplace=True)  # filling boolean with False
    df['trafficSource.adwordsClickInfo.isVideoAd'].fillna(True, inplace=True)  # filling boolean with True
    df.loc[df['geoNetwork.city'] == "(not set)", 'geoNetwork.city'] = np.nan
    df['geoNetwork.city'].fillna("NaN", inplace=True)
    df["totals.transactionRevenue"] = df["totals.transactionRevenue"].fillna(0.0).astype(float)  # filling NA with zero
    df['totals.pageviews'] = df['totals.pageviews'].astype(int)  # setting numerical column as integer
    df['totals.newVisits'] = df['totals.newVisits'].astype(int)  # setting numerical column as integer
    df['totals.bounces'] = df['totals.bounces'].astype(int)  # setting numerical column as integer
    df["totals.hits"] = df["totals.hits"].astype(float)  # setting numerical to float
    df['totals.visits'] = df['totals.visits'].astype(int)  # setting as int

    return df  # return the transformed dataframe


def normalizing(df):
    # Use MinMax Scale to normalize the column
    df["totals.hits"] = (df['totals.hits'] - min(df['totals.hits'])) / (max(df['totals.hits']) - min(df['totals.hits']))
    # normalizing the transaction Revenue
    df['totals.transactionRevenue'] = df['totals.transactionRevenue'].apply(lambda x: np.log1p(x))
    # return the modified df
    return df


def discovering_constant_columns(df=None):
    # discovering_consts = [col for col in df.columns if df[col].nunique() == 1]
    #
    # # printing the total of columns dropped and the name of columns
    # print("Columns with just one value: ", len(discovering_consts), "columns")
    # print("Name of constant columns: ", discovering_consts)

    to_drop = ["socialEngagementType", 'device.browserVersion', 'device.browserSize', 'device.flashVersion',
               'device.language', 'device.mobileDeviceBranding', 'device.mobileDeviceInfo',
               'device.mobileDeviceMarketingName', 'device.mobileDeviceModel', 'device.mobileInputSelector',
               'device.operatingSystemVersion', 'device.screenColors', 'device.screenResolution',
               'geoNetwork.cityId', 'geoNetwork.latitude', 'geoNetwork.longitude', 'geoNetwork.networkLocation',
               'trafficSource.adwordsClickInfo.criteriaParameters', 'trafficSource.adContent']
    return to_drop


def show_data(df, data_type=object, limit=3):  # setting the function with df,
    n = df.select_dtypes(include=data_type)  # selecting the desired data type
    for column in n.columns:  # initializing the loop
        print("Name of column ", column, ': \n', "Uniques: ", df[column].unique()[:limit], "\n",
              " | ## Total nulls: ", (round(df[column].isnull().sum() / len(df[column]) * 100, 2)),
              " | ## Total unique values: ", df.nunique()[column])  # print the data and % of nulls)
        # print("Percent of top 3 of: ", column)
        # print(round(df[column].value_counts()[:3] / df[column].value_counts().sum() * 100,2))
        print("#############################################")


def drop_constant_columns(df, to_drop):
    print("Total features dropped: ", len(to_drop))
    print("Shape before dropping: ", df.shape)
    for column in to_drop:
        if "totals" not in column:
            df.drop(column, axis=1, inplace=True)
    print("Shape after dropping: ", df.shape)
    return df


def replace_huge_string(df):
    string_to_change = ['not available in demo dataset', '(not set)',
                        '(not provided)', '(none)', 'unknown.unknown', 'unknown']
    for string in string_to_change:
        df = df.replace(string, '')
    return df


def date_process(df):
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")  # setting the column as pandas datetime
    df["_weekday"] = df['date'].dt.weekday  # extracting week day
    df["_day"] = df['date'].dt.day  # extracting day
    df["_month"] = df['date'].dt.month  # extracting day
    df["_year"] = df['date'].dt.year  # extracting day
    df['_visitHour'] = (df['visitStartTime'].apply(lambda x: str(datetime.fromtimestamp(x).hour))).astype(int)
    return df  # returning the df after the transformations


def add_date_features(df):
    df['date'] = pd.to_datetime(df['visitStartTime'], unit='s')
    df['sess_date_dow'] = df['date'].dt.dayofweek
    df['sess_date_hours'] = df['date'].dt.hour
    df['sess_date_dom'] = df['date'].dt.day
    return df
