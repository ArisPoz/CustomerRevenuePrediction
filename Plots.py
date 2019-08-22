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
    ui.add_tab("Revenue Graph", figure, 0, "Only 23% Of The Visits\nAre Actually Giving Revenue")
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_device_browser(ui, df):
    # the top 10 of browsers represent % of total
    tooltip = "Percentage of Browser usage: \n"
    tooltip += str(df['device.browser'].value_counts()[:7])
    ui.append_console(tooltip)  # printing the top 7 percentage of browsers
    top_value = df['device.browser'].value_counts().idxmax()
    ui.line_Browser.setText(top_value.capitalize())
    top_value = df['device.deviceCategory'].value_counts().idxmax()
    ui.line_Device.setText(top_value.capitalize())
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
    plt.xticks(rotation=20)  # Adjust the x ticks, rotating the labels
    ui.add_tab("Device Browser", figure, 1, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_cross_revenue_browser(ui, df):
    # It's another way to plot our data. using a variable that contains the plot parameters
    figure = plt.figure(figsize=(6, 4))
    g1 = sns.boxenplot(x='device.browser', y='totals.transactionRevenue',
                       data=df[(df['device.browser'].isin(
                           df['device.browser'].value_counts()[:10].index.values)) &
                               df['totals.transactionRevenue'] > 0])
    plt.title('Browsers by Transactions Revenue', fontsize=20)  # title and fontsize
    g1.set_xlabel(g1.get_xticklabels(),
                  rotation=20)  # It's the way to rotate the x ticks when we use variable to our graphs
    plt.xlabel('Device Names', fontsize=12)  # x label
    plt.ylabel('Trans Revenue(log) Dist', fontsize=12)  # y label
    plt.xticks(rotation=20)
    ui.add_tab("Revenue X Browser", figure, 2, "Revenue By Browser")
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_channel_grouping(ui, df):
    # the top 10 of browsers represent % of total
    tooltip = "Percentage of Channel Grouping used: \n"
    tooltip += str((df['channelGrouping'].value_counts()[:5]))
    ui.append_console(tooltip)  # printing the top 7 percentage of browsers
    top_value = df['channelGrouping'].value_counts().idxmax()
    ui.line_Channel.setText(top_value.capitalize())
    top_value = df['trafficSource.source'].value_counts().idxmax()
    ui.line_Source.setText(top_value.capitalize())
    top_value = df["geoNetwork.networkDomain"].value_counts().idxmax()
    ui.line_Network.setText(top_value.capitalize())
    figure = plt.figure(figsize=(6, 4))
    # let explore the browser used by users
    sns.countplot(df["channelGrouping"], palette="hls")  # It's a module to count the category's
    plt.title("Channel Grouping Count", fontsize=20)  # setting the title size
    plt.xlabel("Channel Grouping Name", fontsize=12)  # setting the x label size
    plt.ylabel("Count", fontsize=12)  # setting the y label size
    ui.add_tab("Channel Grouping", figure, 3, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def show_operating_systems(ui, df):
    # the top 5 of browsers represent % of total
    tooltip = "Percentage of Operational System: \n"
    tooltip += str(df['device.operatingSystem'].value_counts()[:5])
    ui.append_console(tooltip)  # printing the top 7 percentage of browsers
    top_value = df['device.operatingSystem'].value_counts().idxmax()
    ui.line_OS.setText(top_value.capitalize())
    figure = plt.figure(figsize=(6, 4))
    # let explore the browser used by users
    sns.countplot(df["device.operatingSystem"], palette="hls")  # It's a module to count the category's
    plt.title("Operational System used Count", fontsize=20)  # setting the title size
    plt.xlabel("Operational System Name", fontsize=12)  # setting the x label size
    plt.ylabel("OS Count", fontsize=12)  # setting the y label size
    plt.xticks(rotation=20)  # Adjust the x ticks, rotating the labels
    ui.add_tab("OS", figure, 4, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def transaction_by_os(ui, df):
    tooltip = "Transaction by OS"
    figure = plt.figure(figsize=(6, 4))
    figure.suptitle("Transactions By OS", fontsize=20)
    figure.subplots_adjust(top=0.93, wspace=0.3)

    ax = figure.add_subplot(1, 1, 1)
    ax.set_xlabel("Sulphates")
    ax.set_ylabel("Frequency")

    g = sns.FacetGrid(df[(df['device.operatingSystem']
                          .isin(df['device.operatingSystem']
                                .value_counts()[:6].index.values)) & df['totals.transactionRevenue'] > 0],
                      hue='device.operatingSystem', palette="hls")
    g.map(sns.kdeplot, 'totals.transactionRevenue', shade=True, ax=ax)

    ax.legend(title='Type')
    ui.add_tab("Transaction by OS", figure, 5, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def frequent_subcontinents(ui, df):
    # the top 8 of browsers represent % of total
    tooltip = "Description of SubContinent count: \n"
    tooltip += str(df['geoNetwork.subContinent'].value_counts()[:8])
    ui.append_console(tooltip)  # printing the top 7 percentage of browsers
    figure = plt.figure(figsize=(6, 4))
    top_value = df["geoNetwork.subContinent"].value_counts().idxmax()
    ui.line_Continent.setText(top_value.capitalize())
    # let explore the browser used by users
    sns.countplot(df[df['geoNetwork.subContinent']
                  .isin(df['geoNetwork.subContinent']
                        .value_counts()[:15].index.values)]['geoNetwork.subContinent'],
                  palette="hls")  # It's a module to count the category's
    plt.title("TOP 15 most frequent SubContinents", fontsize=20)  # setting the title size
    plt.xlabel("subContinent Names", fontsize=18)  # setting the x label size
    plt.ylabel("SubContinent Count", fontsize=18)  # setting the y label size
    plt.xticks(rotation=20)  # Adjust the x ticks, rotating the labels
    ui.add_tab("SubContinents", figure, 8, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


number_of_colors = 20
color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
         for i in range(number_of_colors)]


def top_countries(ui, df):
    country_tree = df["geoNetwork.country"].value_counts()  # counting the values of Country
    tooltip = "Description most frequent countries: \n"
    tooltip += str(country_tree[:15])
    ui.append_console(tooltip)  # printing the 15 top most
    top_value = df["geoNetwork.country"].value_counts().idxmax()
    ui.line_Country.setText(top_value.capitalize())
    figure = plt.figure(figsize=(6, 4))
    country_tree = round((df["geoNetwork.country"].value_counts()[:30]
                          / len(df['geoNetwork.country']) * 100), 2)

    g = squarify.plot(sizes=country_tree.values, label=country_tree.index,
                      value=country_tree.values,
                      alpha=.4, color=color)
    g.set_title("'TOP 30 Countries (%)", fontsize=20)
    g.set_axis_off()
    ui.add_tab("Countries", figure, 7, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def top_cities(ui, df):
    city_tree = df["geoNetwork.city"].value_counts()  # counting
    tooltip = "Description most frequent Cities: \n"
    tooltip += str(city_tree[:15])
    ui.append_console(tooltip)
    top_value = df["geoNetwork.city"].value_counts().idxmax()
    ui.line_City.setText(top_value.capitalize())
    figure = plt.figure(figsize=(6, 4))
    city_tree = round((city_tree[:30] / len(df['geoNetwork.city']) * 100), 2)

    g = squarify.plot(sizes=city_tree.values, label=city_tree.index,
                      value=city_tree.values,
                      alpha=.4, color=color)
    g.set_title("'TOP 30 Cities (%)", fontsize=20)
    g.set_axis_off()
    ui.add_tab("Cities", figure, 6, tooltip)
    ui.update_progressbar(ui.get_progressbar_status() + 1)


def display_feature_importance(ui, importance):
    importance['gain_log'] = np.log1p(importance['gain'])
    mean_gain = importance[['gain', 'feature']].groupby('feature').mean()
    importance['mean_gain'] = importance['feature'].map(mean_gain['gain'])

    figure = plt.figure(figsize=(8, 12))
    figure.suptitle("Transactions By OS", fontsize=20)
    figure.subplots_adjust(top=0.93, wspace=0.3)

    ax = figure.add_subplot(1, 1, 1)
    ax.set_xlabel("Sulphates")
    ax.set_ylabel("Frequency")
    sns.barplot(x='gain_log', y='feature', data=importance.sort_values('mean_gain', ascending=False), ax=ax)
    ui.add_tab("Valuable Columns", figure, 9, "Feature Importance")
    return plt
