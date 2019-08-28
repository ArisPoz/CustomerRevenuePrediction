import numpy as np
from sklearn import model_selection, preprocessing, metrics
import lightgbm as lgb
import warnings
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GroupKFold
import Plots as showPlots
import datetime
import pandas as pd

warnings.simplefilter('ignore', FutureWarning)


def predict_revenue_at_session_level(ui, train_df, test_df):
    print("Variables not in test but in train : ", set(train_df.columns).difference(set(test_df.columns)))
    train_df = train_df.drop(["trafficSource.campaignCode"], axis=1)

    # Impute 0 for missing target values
    train_df["totals.transactionRevenue"].fillna(0, inplace=True)
    train_y = train_df["totals.transactionRevenue"].values
    train_id = train_df["fullVisitorId"].values
    test_id = test_df["fullVisitorId"].values

    # label encode the categorical variables and convert the numerical variables to float
    cat_cols = ["channelGrouping", "device.browser", "device.deviceCategory", "device.operatingSystem",
                "geoNetwork.city", "geoNetwork.continent", "geoNetwork.country", "geoNetwork.metro",
                "geoNetwork.networkDomain", "geoNetwork.region", "geoNetwork.subContinent",
                "trafficSource.adwordsClickInfo.adNetworkType", 'trafficSource.adwordsClickInfo.gclId',
                "trafficSource.medium", "trafficSource.source", 'trafficSource.adwordsClickInfo.isVideoAd',
                'trafficSource.isTrueDirect', 'trafficSource.campaign', 'trafficSource.adwordsClickInfo.page',
                'trafficSource.referralPath', 'trafficSource.adwordsClickInfo.slot', 'trafficSource.keyword']

    for col in cat_cols:
        print(col)
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train_df[col].values.astype('str')) + list(test_df[col].values.astype('str')))
        train_df[col] = lbl.transform(list(train_df[col].values.astype('str')))
        test_df[col] = lbl.transform(list(test_df[col].values.astype('str')))
        ui.update_progressbar(ui.get_progressbar_status() + 1)

    num_cols = ["totals.hits", "totals.pageviews", "visitNumber", "visitStartTime", 'totals.bounces',
                'totals.newVisits']
    for col in num_cols:
        train_df[col] = train_df[col].astype(float)
        test_df[col] = test_df[col].astype(float)

    train_df['date'] = pd.to_datetime(train_df['date'], format='%Y/%m/%d')
    # Split the train dataset into development and valid based on time
    dev_df = train_df[train_df['date'] <= datetime.date(2017, 5, 31)]
    val_df = train_df[train_df['date'] > datetime.date(2017, 5, 31)]
    dev_y = np.log1p(dev_df["totals.transactionRevenue"].values)
    val_y = np.log1p(val_df["totals.transactionRevenue"].values)

    dev_X = dev_df[cat_cols + num_cols]
    val_X = val_df[cat_cols + num_cols]
    test_X = test_df[cat_cols + num_cols]

    # custom function to run light gbm model
    def run_lgb(train_X, train_y, val_X, val_y, test_X):
        params = {
            "objective": "regression",
            "metric": "rmse",
            "num_leaves": 30,
            "min_child_samples": 100,
            "learning_rate": 0.1,
            "bagging_fraction": 0.7,
            "feature_fraction": 0.5,
            "bagging_frequency": 5,
            "bagging_seed": 2018,
            "verbosity": -1
        }

        lgtrain = lgb.Dataset(train_X, label=train_y)
        lgval = lgb.Dataset(val_X, label=val_y)
        model = lgb.train(params, lgtrain, 1000, valid_sets=[lgval], early_stopping_rounds=1000, verbose_eval=1000)

        pred_test_y = model.predict(test_X, num_iteration=model.best_iteration)
        pred_val_y = model.predict(val_X, num_iteration=model.best_iteration)
        return pred_test_y, model, pred_val_y

    # Training the model #
    pred_test, model, pred_val = run_lgb(dev_X, dev_y, val_X, val_y, test_X)

    pred_val[pred_val < 0] = 0
    val_pred_df = pd.DataFrame({"fullVisitorId": val_df["fullVisitorId"].values})
    val_pred_df["transactionRevenue"] = val_df["totals.transactionRevenue"].values
    val_pred_df["PredictedRevenue"] = np.expm1(pred_val)
    val_pred_df = val_pred_df.groupby("fullVisitorId")["transactionRevenue", "PredictedRevenue"].sum().reset_index()
    value = np.sqrt(metrics.mean_squared_error(np.log1p(val_pred_df["transactionRevenue"].values),
                                               np.log1p(val_pred_df["PredictedRevenue"].values)))
    print(value)

    sub_df = pd.DataFrame({"fullVisitorId": test_id})
    pred_test[pred_test < 0] = 0
    sub_df["PredictedLogRevenue"] = np.expm1(pred_test)
    sub_df = sub_df.groupby("fullVisitorId")["PredictedLogRevenue"].sum().reset_index()
    sub_df.columns = ["fullVisitorId", "PredictedLogRevenue"]
    sub_df["PredictedLogRevenue"] = np.log1p(sub_df["PredictedLogRevenue"])
    sub_df.to_csv("DataSets/prediction.csv", index=False)

    showPlots.display_feature_importance(ui, model)

    return round(value, 5)
