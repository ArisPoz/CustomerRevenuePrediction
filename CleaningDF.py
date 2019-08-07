import pandas as pd
import numpy as np


def filling_na_values(df):  # fillna numeric feature
    df['totals.pageviews'].fillna(1, inplace=True)  # filling NA's with 1
    df['totals.newVisits'].fillna(0, inplace=True)  # filling NA's with 0
    df['totals.bounces'].fillna(0, inplace=True)  # filling NA's with 0
    df["totals.transactionRevenue"] = df["totals.transactionRevenue"].fillna(0.0)  # filling NA with zero
    df['trafficSource.isTrueDirect'].fillna(False, inplace=True)  # filling boolean with False
    df['trafficSource.adwordsClickInfo.isVideoAd'].fillna(True, inplace=True)  # filling boolean with True
    df.loc[df['geoNetwork.city'] == "(not set)", 'geoNetwork.city'] = np.nan
    df['geoNetwork.city'].fillna("NaN", inplace=True)

    return df  # return the transformed dataframe


def discovering_constant_columns(df):
    discovering_consts = [col for col in df.columns if df[col].nunique() == 1]

    # printing the total of columns dropped and the name of columns
    print("Columns with just one value: ", len(discovering_consts), "columns")
    print("Name of constant columns: \n", discovering_consts)
    return discovering_consts


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
    for column in to_drop:
        if "totals" in column:
            df.drop(column, axis=1, inplace=True)
    return df
