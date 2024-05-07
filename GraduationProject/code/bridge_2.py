import numpy as np
import pandas as pd
from lightning.pytorch.callbacks import EarlyStopping
from pytorch_forecasting import TimeSeriesDataSet, GroupNormalizer, TemporalFusionTransformer, QuantileLoss, Baseline
from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint
import lightning.pytorch as pl
from lightning.pytorch.loggers import TensorBoardLogger
import torch
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

max_encoder_length = 30
# set history window
max_prediction_length = 90
# muti-number prediction
training_cutoff = int(df.iloc[-1,-2]) - max_prediction_length

training = TimeSeriesDataSet(
    data=df.iloc[-3660:-366,:],
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
batch_size = 32
train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=0)

# actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
# baseline_predictions = Baseline().predict(val_dataloader)
# (actuals - baseline_predictions).abs().mean().item()

early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=5, verbose=True, mode="min")
lr_logger = LearningRateMonitor()
logger = TensorBoardLogger("lightning_logs")

checkpoint_callback = ModelCheckpoint(
    monitor='val_loss',
    dirpath=r'C:\Users\Dennis\Desktop\TFT_model',
#    filename='{epoch}-{val_loss:.2f}-{other_metric:.2f}')
    filename='bridge')

trainer = pl.Trainer(
    max_epochs=45,
    devices=1,
    enable_model_summary=True,
    gradient_clip_val=0.1,
    callbacks=[lr_logger, early_stop_callback,checkpoint_callback],
    logger=logger,)

tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.001,
    # often change
    #hidden_size=160,
    hidden_size=320,
    attention_head_size=4,
    dropout=0.1,
    #hidden_continuous_size=160,
    hidden_continuous_size=320,
    output_size=7,
    loss=QuantileLoss(),
    log_interval=10,
    reduce_on_plateau_patience=4)

trainer.fit(
    tft,
    train_dataloaders=train_dataloader,
    val_dataloaders=val_dataloader)

best_model_path = r"C:\Users\Dennis\Desktop\TFT_model\bridge.ckpt"
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
best_tft.eval()
actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
act_np = actuals.numpy()
act_np = act_np[0]
predictions = best_tft.predict(val_dataloader)
pre_np = predictions.numpy()
pre_np = pre_np[0]
gap = (actuals - predictions).abs().mean().item()
x = np.arange(1, len(pre_np) + 1)
plt.plot(x,act_np,  color='blue', label='Actual')
plt.plot(x,pre_np,  color='red', label='Prediction')
plt.plot(x,abs(pre_np-act_np),  color='green', label='Loss')

plt.legend()
plt.xlabel('Value')
plt.ylabel('Sequence')
plt.title('Line Plot of Actual and Prediction')
plt.show()
# raw_predictions = best_tft.predict(val_dataloader, mode="raw", return_x=True)
# print(raw_predictions._fields)
print("batch=",batch_size,"max_encoder_length =",max_encoder_length,"max_prediction_length =",max_prediction_length)
# raw_predictions, x = best_tft.predict(val_dataloader, mode="raw", return_x=True)
# interpretation = best_tft.interpret_output(raw_predictions, reduction="sum")
# best_tft.plot_interpretation(interpretation)
# 14.29good
# try change output_size
print("act=",act_np)
print("pre=",pre_np)
print("bridge")