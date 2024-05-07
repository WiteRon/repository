import numpy as np
import pandas as pd
from pytorch_forecasting import TimeSeriesDataSet, GroupNormalizer, TemporalFusionTransformer, QuantileLoss, Baseline
import torch
import matplotlib.pyplot as plt



data = pd.read_csv('multipleClimateData.csv', index_col=0)
data = data.iloc[:,0:5]
data.index = pd.to_datetime(data.index)
data.sort_index(inplace=True)
df = data
# print(data.head(10))
earliest_time = df.index.min()

df['days_from_start'] = (df.index - earliest_time).days
# print(df.head(10).iloc[:,2])
letter_dict = {}
for i in range(ord('A'), ord('Z') + 1):
    letter_dict[chr(i)] = i - ord('A') + 1

df.iloc[:, 2] = df.iloc[:, 2].map(letter_dict)
# print(df.head(10).iloc[:,2])
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
# print(df.columns)
# print(df.head(10))

max_encoder_length = 7
# set history window
max_prediction_length = 90
# muti-number prediction
training_cutoff = int(df.iloc[-1,-2]) - max_prediction_length

training = TimeSeriesDataSet(
    data=df.iloc[-7686:-366,:],
    # set dataset for training
    time_idx="days_from_start",
    target="TEMP",
    min_encoder_length=max_encoder_length // 2,
    max_encoder_length=max_encoder_length,
    min_prediction_length=1,
    max_prediction_length=max_prediction_length,
    time_varying_known_reals=["DATE",'FRSHTT',"days_from_start"],
    time_varying_unknown_reals=['PRCP','TEMP_ATTRIBUTES', 'TEMP'],
    add_relative_time_idx=True,
    add_target_scales=False,
    group_ids=["Group"],
    # add_encoder_length=True,
    allow_missing_timesteps=True,

)

validation = TimeSeriesDataSet.from_dataset(training, df, predict=True, stop_randomization=True)
batch_size = 64
train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=0)

best_model_path = r"C:\Users\Dennis\Desktop\TFT_model\formal_1.ckpt"
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
best_tft.eval()
actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
act_np = actuals.numpy()
act_np = act_np[0]
predictions = best_tft.predict(val_dataloader)
pre_np = predictions.numpy()
pre_np = pre_np[0]
gap = (actuals - predictions).abs().mean().item()
print(gap)
x = np.arange(1, len(pre_np) + 1)
plt.plot(x,act_np,  color='blue', label='Actual')
plt.plot(x,pre_np,  color='red', label='Prediction')
plt.plot(x,abs(pre_np-act_np),  color='green', label='Loss')

plt.legend()
plt.xlabel('Value')
plt.ylabel('Sequence')
plt.title('Line Plot of Actual and Prediction')
plt.show()

