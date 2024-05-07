import torch
import torch.nn as nn
from torch.optim import SGD
import numpy as np
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
import pandas as pd
import math



# 手搓线性回归Test 1

# 1.数据准备y = 3x + 0.8
x = torch.rand([500,1])
y_true = 3 * x + 0.8
learning_rate = 0.01
# 2.计算y_predict
w = torch.rand([1,1],requires_grad=True)
b = torch.tensor(0,requires_grad=True,dtype=torch.float32)

# 4.反向传播
for i in range(2500):
    # 3.计算loss
    y_predict = torch.matmul(x, w) + b
    loss = (y_true - y_predict).pow(2).mean()
    if w.grad is not None:
        w.grad.data.zero_()
    if b.grad is not None:
        b.grad.data.zero_()

    loss.backward()
    w.data = w.data - w.grad * learning_rate
    b.data = b.data - learning_rate * b.grad
    if i%50 == 0 :
        print("w,b,loss", w.item(), b.item(), loss.item())

plt.figure(figsize=(20,8))
plt.scatter(x.numpy().reshape(-1),y_true.numpy().reshape(-1))
y_predict = torch.matmul(x, w) + b
plt.plot(x.numpy().reshape(-1),y_predict.detach().numpy().reshape(-1),c = "r")
plt.show()
