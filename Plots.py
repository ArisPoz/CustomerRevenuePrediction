import random

import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import squarify
import seaborn as sns
import pandas as pd

"""
Created on Thu Aug 8 14:30:52 2019

@author: apozidis
"""


def show_revenue_graph(ui, df):
    figure = plt.figure(figsize=(6, 4))
    plt.scatter(range(df.shape[0]), np.sort(df["totals.transactionRevenue"].values))
    plt.xlabel('index', fontsize=12)
    plt.ylabel('TransactionRevenue', fontsize=12)
    plt.title('The 80/20 rule', fontsize=20)
    ui.add_tab("Revenue Graph", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_device_browser(ui, df):
    # the top 10 of browsers represent % of total
    print("Percentage of Browser usage: ")
    print(df['device.browser'].value_counts()[:7])  # printing the top 7 percentage of browsers
    top_value = df['device.browser'].value_counts().idxmax()
    ui.line_Browser.setText(top_value)
    top_value = df['device.deviceCategory'].value_counts().idxmax()
    ui.line_Device.setText(top_value)
    # setting the graph size
    figure = plt.figure(figsize=(6, 4))

    # Let explore the browser used by users
    sns.countplot(df[df['device.browser']
                  .isin(df['device.browser']
                        .value_counts()[:10].index.values)]['device.browser'],
                  palette="hls")  # It's a module to count the category's
    plt.title("TOP 10 Most Frequent Browsers", fontsize=20)  # Adding Title and setting the size
    plt.xlabel("Browser Names", fontsize=12)  # Adding x label and setting the size
    plt.ylabel("Count", fontsize=12)  # Adding y label and setting the size
    plt.xticks(rotation=45)  # Adjust the x ticks, rotating the labels
    ui.add_tab("Device Browser", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_cross_revenue_browser(ui, df):
    # It's another way to plot our data. using a variable that contains the plot parameters
    figure = plt.figure(figsize=(6, 4))
    g1 = sns.boxenplot(x='device.browser', y='totals.transactionRevenue',
                       data=df[(df['device.browser'].isin(
                           df['device.browser'].value_counts()[:10].index.values)) &
                               df['totals.transactionRevenue'] > 0])
    plt.title('Browsers Name by Transactions Revenue', fontsize=20)  # title and fontsize
    g1.set_xlabel(g1.get_xticklabels(),
                  rotation=45)  # It's the way to rotate the x ticks when we use variable to our graphs
    plt.xlabel('Device Names', fontsize=12)  # x label
    plt.ylabel('Trans Revenue(log) Dist', fontsize=12)  # y label
    plt.xticks(rotation=45)
    ui.add_tab("Revenue Cross Browser", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_channel_grouping(ui, df):
    # the top 10 of browsers represent % of total
    print("Percentage of Channel Grouping used: ")
    print((df['channelGrouping'].value_counts()[:5]))  # printing the top 7 percentage of browsers
    top_value = df['channelGrouping'].value_counts().idxmax()
    ui.line_Channel.setText(top_value)
    top_value = df['trafficSource.source'].value_counts().idxmax()
    ui.line_Source.setText(top_value)
    top_value = df["geoNetwork.networkDomain"].value_counts().idxmax()
    ui.line_Network.setText(top_value)
    figure = plt.figure(figsize=(6, 4))
    # let explore the browser used by users
    sns.countplot(df["channelGrouping"], palette="hls")  # It's a module to count the category's
    plt.title("Channel Grouping Count", fontsize=20)  # setting the title size
    plt.xlabel("Channel Grouping Name", fontsize=12)  # setting the x label size
    plt.ylabel("Count", fontsize=12)  # setting the y label size
    ui.add_tab("Channel Grouping", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_operating_systems(ui, df):
    # the top 5 of browsers represent % of total
    print("Percentage of Operational System: ")
    print(df['device.operatingSystem'].value_counts()[:5])  # printing the top 7 percentage of browsers
    top_value = df['device.operatingSystem'].value_counts().idxmax()
    ui.line_OS.setText(top_value)
    figure = plt.figure(figsize=(6, 4))
    # let explore the browser used by users
    sns.countplot(df["device.operatingSystem"], palette="hls")  # It's a module to count the category's
    plt.title("Operational System used Count", fontsize=20)  # setting the title size
    plt.xlabel("Operational System Name", fontsize=12)  # setting the x label size
    plt.ylabel("OS Count", fontsize=12)  # setting the y label size
    plt.xticks(rotation=45)  # Adjust the x ticks, rotating the labels
    ui.add_tab("OS", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def transaction_by_os(ui, df):
    figure = plt.figure(figsize=(6, 4))
    g = sns.FacetGrid(df[(df['device.operatingSystem']
                          .isin(df['device.operatingSystem']
                                .value_counts()[:6].index.values)) & df['totals.transactionRevenue'] > 0],
                      hue='device.operatingSystem', palette="hls").map(sns.kdeplot,
                                                                       'totals.transactionRevenue',
                                                                       shade=True)
    plt.title("Transactions By OS", fontsize=20)
    ui.add_tab("Transaction by OS", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def frequent_subcontinents(ui, df):
    # the top 8 of browsers represent % of total
    print("Description of SubContinent count: ")
    print(df['geoNetwork.subContinent'].value_counts()[:8])  # printing the top 7 percentage of browsers
    figure = plt.figure(figsize=(6, 4))
    top_value = df["geoNetwork.subContinent"].value_counts().idxmax()
    ui.line_Continent.setText(top_value)
    # let explore the browser used by users
    sns.countplot(df[df['geoNetwork.subContinent']
                  .isin(df['geoNetwork.subContinent']
                        .value_counts()[:15].index.values)]['geoNetwork.subContinent'],
                  palette="hls")  # It's a module to count the category's
    plt.title("TOP 15 most frequent SubContinents", fontsize=20)  # setting the title size
    plt.xlabel("subContinent Names", fontsize=18)  # setting the x label size
    plt.ylabel("SubContinent Count", fontsize=18)  # setting the y label size
    plt.xticks(rotation=45)  # Adjust the x ticks, rotating the labels
    ui.add_tab("Top Cities", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


number_of_colors = 20
color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
         for i in range(number_of_colors)]


def top_countries(ui, df):
    country_tree = df["geoNetwork.country"].value_counts()  # counting the values of Country

    print("Description most frequent countries: ")
    print(country_tree[:15])  # printing the 15 top most
    top_value = df["geoNetwork.country"].value_counts().idxmax()
    ui.line_Country.setText(top_value)
    figure = plt.figure(figsize=(6, 4))
    country_tree = round((df["geoNetwork.country"].value_counts()[:30]
                          / len(df['geoNetwork.country']) * 100), 2)

    g = squarify.plot(sizes=country_tree.values, label=country_tree.index,
                      value=country_tree.values,
                      alpha=.4, color=color)
    g.set_title("'TOP 30 Countries - % size of total", fontsize=20)
    g.set_axis_off()
    ui.add_tab("Top Countries", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def top_cities(ui, df):
    city_tree = df["geoNetwork.city"].value_counts()  # counting

    print("Description most frequent Cities: ")
    print(city_tree[:15])
    top_value = df["geoNetwork.city"].value_counts().idxmax()
    ui.line_City.setText(top_value)
    figure = plt.figure(figsize=(6, 4))
    city_tree = round((city_tree[:30] / len(df['geoNetwork.city']) * 100), 2)

    g = squarify.plot(sizes=city_tree.values, label=city_tree.index,
                      value=city_tree.values,
                      alpha=.4, color=color)
    g.set_title("'TOP 30 Cities - % size of total", fontsize=20)
    g.set_axis_off()
    ui.add_tab("Freq SubContinents", figure)
    ui.update_progressbar(ui.get_progressbar_status() + 1)
