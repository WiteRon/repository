import numpy as np
import pandas as pd
from lightning.pytorch.callbacks import EarlyStopping
from pytorch_forecasting import TimeSeriesDataSet, GroupNormalizer, TemporalFusionTransformer, QuantileLoss, Baseline
from lightning.pytorch.callbacks import LearningRateMonitor
import lightning.pytorch as pl
from lightning.pytorch.loggers import TensorBoardLogger
import torch

best_model_path = r"C:\Users\Dennis\Desktop\TFT_model\epoch=0-val_loss=3.51-other_metric=0.00.ckpt"
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)

print(best_tft)
