# 纯Python实现
from time import time
from math import exp, sqrt, log
from random import gauss, seed


seed(2000)
# 计算的一些初始值
S_0 = 100.0    # 股票或指数初始的价格;
K = 105        #  行权价格
T = 1.0        #  期权的到期年限(距离到期日时间间隔)
r = 0.05       #   无风险利率
sigma = 0.2    # 波动率(收益标准差)
M = 50         # number of time steps
dt = T/M       # time enterval
I = 20000       # number of simulation

start = time()
S = []     #
for i in range(I):
    path = []    # 时间间隔上的模拟路径
    for t in range(M+1):
        if t == 0:
            path.append(S_0)
        else:
            z = gauss(0.0, 1.0)
            S_t = path[t-1] * exp((r-0.5*sigma**2) * dt + sigma * sqrt(dt) * z)
            path.append(S_t)
    S.append(path)
# 计算期权现值
C_0 = exp(-r * T) * sum([max(path[-1] - K, 0) for path in S])/I
total_time = time() - start
print('European Option value %.6f' % C_0)
print('total time is %.6f seconds' % total_time)
