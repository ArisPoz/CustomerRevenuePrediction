import numpy as np
from sklearn import model_selection, preprocessing, metrics
import lightgbm as lgb
import warnings
from sklearn.model_selection import GroupKFold
import datetime
import pandas as pd

warnings.simplefilter('ignore', FutureWarning)


def get_folds(ui, df=None, n_splits=5):
    """Returns dataframe indices corresponding to Visitors Group KFold"""
    # Get sorted unique visitors
    unique_vis = np.array(sorted(df['fullVisitorId'].astype(str).unique()))

    # Get folds
    folds = GroupKFold(n_splits=n_splits)
    fold_ids = []
    ids = np.arange(df.shape[0])
    for trn_vis, val_vis in folds.split(X=unique_vis, y=unique_vis, groups=unique_vis):
        fold_ids.append(
            [
                ids[df['fullVisitorId'].isin(unique_vis[trn_vis])],
                ids[df['fullVisitorId'].isin(unique_vis[val_vis])]
            ]
        )
        ui.update_progressbar(ui.get_progressbar_status() + 1)

    return fold_ids


def get_session_target(train, test):
    y_reg = train['totals.transactionRevenue'].fillna(0)
    del train['totals.transactionRevenue']

    if 'totals.transactionRevenue' in test.columns:
        del test['totals.transactionRevenue']

    return y_reg


def create_feature_list(train, test):
    excluded_features = [
        'date', 'fullVisitorId', 'sessionId', 'totals.transactionRevenue',
        'visitId', 'visitStartTime', 'trafficSource.campaignCode'
    ]

    categorical_features = [
        _f for _f in train.columns
        if (_f not in excluded_features) & (train[_f].dtype == 'object')
    ]

    return excluded_features, categorical_features


def predict_revenue_at_session_level(ui, train, test_df):
    print("Variables not in test but in train : ", set(train.columns).difference(set(test_df.columns)))
    train_df = train.drop(['trafficSource.campaignCode'], axis=1)

    # Impute 0 for missing target values
    train_df["totals.transactionRevenue"].fillna(0, inplace=True)
    train_y = train_df["totals.transactionRevenue"].values
    train_id = train_df["fullVisitorId"].values
    test_id = test_df["fullVisitorId"].values

    # label encode the categorical variables and convert the numerical variables to float
    cat_cols = ["channelGrouping", "device.browser",
                "device.deviceCategory", "device.operatingSystem", "geoNetwork.city", "geoNetwork.continent",
                "geoNetwork.country", "geoNetwork.metro", "geoNetwork.networkDomain", "geoNetwork.region",
                "geoNetwork.subContinent", "trafficSource.adwordsClickInfo.adNetworkType", "trafficSource.medium",
                "trafficSource.source", 'trafficSource.adwordsClickInfo.isVideoAd', 'trafficSource.isTrueDirect']
    for col in cat_cols:
        print(col)
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train_df[col].values.astype('str')) + list(test_df[col].values.astype('str')))
        train_df[col] = lbl.transform(list(train_df[col].values.astype('str')))
        test_df[col] = lbl.transform(list(test_df[col].values.astype('str')))

    num_cols = ["totals.hits", "totals.pageviews", "visitNumber", "visitStartTime", 'totals.bounces',
                'totals.newVisits', 'totals.visits']
    for col in num_cols:
        train_df[col] = train_df[col].astype(float)
        test_df[col] = test_df[col].astype(float)

    # Split the train dataset into development and valid based on time
    train_df['date'] = pd.to_datetime(train_df['date'], format='%Y/%m/%d %H:%M:%S')
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
            "min_child_samples": 250,
            "learning_rate": 0.03,
            "bagging_fraction": 0.7,
            "feature_fraction": 0.5,
            "bagging_frequency": 5,
            "bagging_seed": 2017,
            "verbosity": -1
        }

        lgtrain = lgb.Dataset(train_X, label=train_y)
        lgval = lgb.Dataset(val_X, label=val_y)
        model = lgb.train(params, lgtrain, 1000, valid_sets=[lgval], early_stopping_rounds=100, verbose_eval=100)

        pred_test_y = model.predict(test_X, num_iteration=model.best_iteration)
        pred_val_y = model.predict(val_X, num_iteration=model.best_iteration)
        return pred_test_y, model, pred_val_y

    # Training the model #
    pred_test, model, pred_val = run_lgb(dev_X, dev_y, val_X, val_y, test_X)

    pred_val[pred_val < 0] = 0
    val_pred_df = pd.DataFrame({"fullVisitorId": val_df["fullVisitorId"].values})
    val_pred_df["transactionRevenue"] = val_df["totals.transactionRevenue"].values
    val_pred_df["PredictedRevenue"] = np.expm1(pred_val)
    value = np.sqrt(metrics.mean_squared_error(np.log1p(val_pred_df["transactionRevenue"].values),
                                               np.log1p(val_pred_df["PredictedRevenue"].values)))
    val_pred_df = val_pred_df.groupby("fullVisitorId")["transactionRevenue", "PredictedRevenue"].sum().reset_index()
    print(np.sqrt(metrics.mean_squared_error(np.log1p(val_pred_df["transactionRevenue"].values),
                                             np.log1p(val_pred_df["PredictedRevenue"].values))))

    return str(round(value, 5))

    # ui.update_progressbar(0)
    # ui.label_PleaseWait.setText("Please wait, while Predicting...")
    # ui.label_PleaseWait.show()
    #
    # excluded_features, categorical_features = create_feature_list(train, test)
    # for f in categorical_features:
    #     train[f], indexer = pd.factorize(train[f])
    #     test[f] = indexer.get_indexer(test[f])
    #     ui.update_progressbar(ui.get_progressbar_status() + 1)
    # train = get_session_target(train, test)
    #
    # folds = get_folds(ui, train, n_splits=5)
    #
    # train_features = [_f for _f in train.columns if _f not in excluded_features]
    # print(train_features)
    #
    # importance = pd.DataFrame()
    # oof_reg_pred = np.zeros(train.shape[0])
    # sub_reg_pred = np.zeros(test.shape[0])
    # for fold_, (trn_, val_) in enumerate(folds):
    #     trn_x, trn_y = train[train_features].iloc[trn_], train.iloc[trn_]
    #     val_x, val_y = train[train_features].iloc[val_], train.iloc[val_]
    #
    #     reg = lgb.LGBMRegressor(
    #         num_leaves=31,
    #         learning_rate=0.03,
    #         n_estimators=1000,
    #         subsample=.9,
    #         colsample_bytree=.9,
    #         random_state=1
    #     )
    #     reg.fit(
    #         trn_x, np.log1p(trn_y),
    #         eval_set=[(val_x, np.log1p(val_y))],
    #         early_stopping_rounds=50,
    #         verbose=100,
    #         eval_metric='rmse'
    #     )
    #     imp_df = pd.DataFrame()
    #     imp_df['feature'] = train_features
    #     imp_df['gain'] = reg.booster_.feature_importance(importance_type='gain')
    #
    #     imp_df['fold'] = fold_ + 1
    #     importance = pd.concat([importance, imp_df], axis=0, sort=False)
    #
    #     oof_reg_pred[val_] = reg.predict(val_x, num_iteration=reg.best_iteration_)
    #     oof_reg_pred[oof_reg_pred < 0] = 0
    #     _pred = reg.predict(test[train_features], num_iteration=reg.best_iteration_)
    #     _pred[_pred < 0] = 0
    #     sub_reg_pred += np.expm1(_pred) / len(folds)
    #     ui.update_progressbar(ui.get_progressbar_status() + 1)
    #     print(oof_reg_pred)
    # print(sub_reg_pred)
    # prediction_score = mean_squared_error(np.log1p(train), oof_reg_pred) ** .5
    # showPlots.display_feature_importance(ui, importance)
    #
    # ui.update_progressbar(100)
    # ui.label_PleaseWait.hide()
