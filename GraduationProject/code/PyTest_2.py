import torch
import torch.nn as nn
from torch.optim import SGD
import numpy as np
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import pandas as pd
import math

'''
def loss_fn(y,y_predict):
    loss = (y_predict - y).pow(2).mean()
    for i in [w,b]:
        if i.grad is not None:
            i.grad.data.zero_()
    loss.backward()
    return loss.data

def optimize(learning_rate):
    w.data -= learning_rate * w.grad.data
    b.data -= learning_rate * w.grad.data

for i in range(3000):
    #2.计算预测值
    y_predict = x * w + b
    #3.计算损失，反向传播
    loss = loss_fn(y,y_predict)
'''
