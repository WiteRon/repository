import pandas as pd
from lightning import Trainer
from lightning.pytorch.callbacks import EarlyStopping
from pytorch_forecasting import TimeSeriesDataSet, GroupNormalizer, TemporalFusionTransformer, QuantileLoss, Baseline, \
    SMAPE
from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint
import lightning.pytorch as pl
from lightning.pytorch.loggers import TensorBoardLogger
# import torch
import matplotlib.pyplot as plt


df = pd.read_csv('processed_data.csv')
max_encoder_length = 3
# set history window
max_prediction_length = 9
# muti-number prediction
training_cutoff = int(df.iloc[-1,-2]) - max_prediction_length

training = TimeSeriesDataSet(
    data=df.iloc[-366:,:],
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

# model = TemporalFusionTransformer.load_from_checkpoint("D:/PyProg/GraduationProject/TFT_model/formal_1.ckpt")
# trainer = Trainer()
# # disable randomness, dropout, etc...
# trainer.fit(model,train_dataloaders=train_dataloader)

# predict with the model
lr_logger = LearningRateMonitor()
logger = TensorBoardLogger("lightning_logs")
early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=5, verbose=True, mode="min")

trainer = pl.Trainer(
    max_epochs=4,  # attention plz
    devices=1,
    enable_model_summary=True,
    gradient_clip_val=0.1,
    callbacks=[lr_logger, early_stop_callback],
    logger=logger,)



# best_model_path = trainer.checkpoint_callback.best_model_path
best_model_path = "D:/PyProg/GraduationProject/TFT_model/formal_1.ckpt"
print(best_model_path)
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
best_tft.eval()

# raw_predictions = best_tft.predict(dataloaders=val_dataloader, mode="raw", return_x=True)
raw_predictions = best_tft.predict(val_dataloader, mode="raw", return_x=True)
print(raw_predictions._fields)
# print((raw_predictions))
best_tft.plot_prediction(raw_predictions.x, raw_predictions.output, idx=0, plot_attention=True,
                         show_future_observed=True,add_loss_to_title=True)
plt.show()

predictions = best_tft.predict(val_dataloader, return_x=True)
predictions_vs_actuals = best_tft.calculate_prediction_actual_by_variable(predictions.x, predictions.output)
best_tft.plot_prediction_actual_by_variable(predictions_vs_actuals)
plt.show()


