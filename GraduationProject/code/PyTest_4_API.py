import torch
import torch.nn as nn
from torch.optim import SGD
import numpy as np
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import pandas as pd
import math


# complete mission using API
x = torch.rand([500,1])
y_true = 3*x + 0.8


class MyLinear(nn.Module):
    def __init__(self):
        super(MyLinear,self).__init__()
        self.linear = nn.Linear(1,1)

    def forward(self, x):
        out = self.linear(x)
        return out


my_linear = MyLinear()
optimizer = SGD(my_linear.parameters(),0.001)
loss_fn = nn.MSELoss()

for i in range(2000):
    y_predict = my_linear(x)
    loss = loss_fn(y_predict,y_true)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if i % 50 == 0:
        params = list(my_linear.parameters())
        print(loss.item(),params[0].item(),params[1].item())
