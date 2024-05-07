# import numpy as np
import pandas as pd
from lightning.pytorch.callbacks import EarlyStopping
from pytorch_forecasting import TimeSeriesDataSet, GroupNormalizer, TemporalFusionTransformer, QuantileLoss, Baseline, \
    SMAPE
from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint
import lightning.pytorch as pl
from lightning.pytorch.loggers import TensorBoardLogger
# import torch
import matplotlib.pyplot as plt


plt.ioff()


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius


def normalize_dataframe(df):
    return (df - df.min()) / (df.max() - df.min()), df.min(), df.max()


def denormalize_dataframe(df_normalized, min_values, max_values):
    return df_normalized * (max_values - min_values) + min_values


data = pd.read_csv('multipleClimateData.csv', index_col=0)
data = data.iloc[:,0:5]
data.index = pd.to_datetime(data.index)
data.sort_index(inplace=True)
df = data
# print(data.head(10))
earliest_time = df.index.min()

df['days_from_start'] = (df.index - earliest_time).days
letter_dict = {}
for i in range(ord('A'), ord('Z') + 1):
    letter_dict[chr(i)] = i - ord('A') + 1

df.iloc[:, 2] = df.iloc[:, 2].map(letter_dict)
print(df.columns)
df.reset_index(drop=False,inplace=True)
df.loc[df['PRCP_ATTRIBUTES'].isnull(), 'PRCP'] = 0
columns = df.columns

last_column = columns[-1]
second_last_column = columns[-2]
columns = list(columns)
columns[-1] = second_last_column
columns[-2] = last_column
df = df[columns]
column_name = 'Group'
df = df.assign(**{column_name: 0})
# df = normalize_dataframe(df)
# df = pd.DataFrame(df)

max_encoder_length = 3
# set history window
max_prediction_length = 9
# muti-number prediction
training_cutoff = int(df.iloc[-1,-2]) - max_prediction_length

# df = df.drop(columns=['DATE'])
df = df.assign(DATE=df['days_from_start'])
df.to_csv('processed_data.csv', index=False)
print('done')
