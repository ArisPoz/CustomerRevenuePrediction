import json
import os
import pandas as pd
from pandas.io.json import json_normalize

train_data_path = "DataSets/train.csv"
test_data_path = "DataSets/test.csv"

JSON_COLUMNS = ['device', 'geoNetwork', 'totals', 'trafficSource']

train_df = pd.read_csv(train_data_path, chunksize=50000,
                       converters={column: json.loads for column in JSON_COLUMNS},
                       dtype={'fullVisitorId': 'str'})

# chunk_List = []
# for chunk in train_df:
#     print(chunk)
#     chunk_List.append(chunk)
#
# df = pd.concat(chunk_List)
#
# for column in JSON_COLUMNS:
#     column_as_df = json_normalize(df[column])
#     column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
#     df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
#     print(f"Loaded {os.path.basename(train_data_path)}. Shape: {df.shape}")
#
#
#
# df.to_csv("DataSets/cleaned_train.csv", index=False)

# df = pd.read_csv(csv_path, chunksize=chunk,
#                  converters={column: json.loads for column in json_columns},
#                  dtype={'fullVisitorId': 'str'})
# for column in json_columns:
#     column_as_df = json_normalize(df[column])
#     column_as_df.columns = [f"{column}.{subcolumn}" for subcolumn in column_as_df.columns]
#     df = df.drop(column, axis=1).merge(column_as_df, right_index=True, left_index=True)
#   print(f"Loaded {os.path.basename(csv_path)}. Shape: {df.shape}")
