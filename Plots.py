import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""
Created on Thu Aug 8 14:30:52 2019

@author: apozidis
"""


def show_revenue_graph(df):
    plt.figure(figsize=(8, 6))
    plt.scatter(range(df.shape[0]), np.sort(df["totals.transactionRevenue"].values))
    plt.xlabel('index', fontsize=12)
    plt.ylabel('TransactionRevenue', fontsize=12)
    plt.title('The 80/20 rule has proven true', fontsize=20)
    plt.show()


def show_device_browser(df):
    # the top 10 of browsers represent % of total
    print("Percentage of Browser usage: ")
    print(df['device.browser'].value_counts()[:7])  # printing the top 7 percentage of browsers

    # setting the graph size
    plt.figure(figsize=(14, 6))

    # Let explore the browser used by users
    sns.countplot(df[df['device.browser'] \
                  .isin(df['device.browser'] \
                        .value_counts()[:10].index.values)]['device.browser'],
                  palette="hls")  # It's a module to count the category's
    plt.title("TOP 10 Most Frequent Browsers", fontsize=20)  # Adding Title and setting the size
    plt.xlabel("Browser Names", fontsize=16)  # Adding x label and setting the size
    plt.ylabel("Count", fontsize=16)  # Adding y label and setting the size
    plt.xticks(rotation=45)  # Adjust the x ticks, rotating the labels
    plt.show()  # use plt.show to render the graph that we did above


def show_cross_revenue_browser(df):
    plt.figure(figsize=(13, 6))  # figure size

    # It's another way to plot our data. using a variable that contains the plot parameters
    g1 = sns.boxenplot(x='device.browser', y='totals.transactionRevenue',
                       data=df[(df['device.browser'].isin(
                           df['device.browser'].value_counts()[:10].index.values)) &
                               df['totals.transactionRevenue'] > 0])
    g1.set_title('Browsers Name by Transactions Revenue', fontsize=20)  # title and fontsize
    g1.set_xticklabels(g1.get_xticklabels(),
                       rotation=45)  # It's the way to rotate the x ticks when we use variable to our graphs
    g1.set_xlabel('Device Names', fontsize=18)  # x label
    g1.set_ylabel('Trans Revenue(log) Dist', fontsize=18)  # y label

    plt.show()


def show_channel_grouping(df):
    # the top 10 of browsers represent % of total
    print("Percentage of Channel Grouping used: ")
    print((df['channelGrouping'].value_counts()[:5]))  # printing the top 7 percentage of browsers

    plt.figure(figsize=(14, 7))  # setting the graph size

    # let explore the browser used by users
    sns.countplot(df["channelGrouping"], palette="hls")  # It's a module to count the category's
    plt.title("Channel Grouping Count", fontsize=20)  # setting the title size
    plt.xlabel("Channel Grouping Name", fontsize=18)  # setting the x label size
    plt.ylabel("Count", fontsize=18)  # setting the y label size

    plt.show()  # use plt.show to render the graph that we did above


def show_channel_cross_browsers(df):
    # I will use the cross tab to explore two categorical values
    # At index I will use set my variable that I want analyse and cross by another
    crosstab_eda = pd.crosstab(index=df['channelGrouping'], normalize=True,
                               # at this line, I am using the isin to select just the top 5 of browsers
                               columns=df[df['device.browser'].isin(df['device.browser'] \
                                                                    .value_counts()[:5].index.values)][
                                   'device.browser'])
    # Plotting the cross tab that we did above
    crosstab_eda.plot(kind="bar",  # select the bar to plot the count of categorical
                      figsize=(14, 7),  # adjusting the size of graphs
                      stacked=True)  # code to unstack
    plt.title("Channel Grouping % for which Browser", fontsize=20)  # setting the title size
    plt.xlabel("The Channel Grouping Name", fontsize=18)  # setting the x label size
    plt.ylabel("Count", fontsize=18)  # setting the y label size
    plt.xticks(rotation=0)
    plt.show()  # rendering


def show_operating_systems(df):
    # the top 5 of browsers represent % of total
    print("Percentage of Operational System: ")
    print(df['device.operatingSystem'].value_counts()[:5])  # printing the top 7 percentage of browsers

    # setting the graph size
    plt.figure(figsize=(14, 7))

    # let explore the browser used by users
    sns.countplot(df["device.operatingSystem"], palette="hls")  # It's a module to count the category's
    plt.title("Operational System used Count", fontsize=20)  # setting the title size
    plt.xlabel("Operational System Name", fontsize=16)  # setting the x label size
    plt.ylabel("OS Count", fontsize=16)  # setting the y label size
    plt.xticks(rotation=45)  # Adjust the x ticks, rotating the labels

    plt.show()  # use plt.show to render the graph that we did above


def show_most_used_browser_by_os(df):
    # At index I will use is in to substitute the loop and get just the values with more than 1%
    cross_tab_eda = pd.crosstab(index=df[df['device.operatingSystem'] \
                                .isin(df['device.operatingSystem'] \
                                      .value_counts()[:6].index.values)]['device.operatingSystem'],

                                # at this line, I am using the is in to select just the top 5 of browsers
                                columns=df[df['device.browser'].isin(df['device.browser'] \
                                                                     .value_counts()[:5].index.values)][
                                    'device.browser'])
    # Plotting the cross tab that we did above
    cross_tab_eda.plot(kind="bar",  # select the bar to plot the count of categorical
                       figsize=(14, 7),  # adjusting the size of graphs
                       stacked=True)  # code to unstack
    plt.title("Most frequent OS's by Browsers of users", fontsize=22)  # adjusting title and fontsize
    plt.xlabel("Operational System Name", fontsize=19)  # adjusting x label and fontsize
    plt.ylabel("Count OS", fontsize=19)  # adjusting y label and fontsize
    plt.xticks(rotation=0)  # Adjust the x ticks, rotating the labels

    plt.show()  # rendering
