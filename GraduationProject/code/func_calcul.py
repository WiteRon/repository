def calcu_HDD(tmp):
    HDD = max(18 - tmp, 0)
    return HDD


def calcu_rwd(tmp_list=None,tem = 1,amount = 2,ini_price = 0,t_days=1):
    if tmp_list is None:
        tmp_list = []
    HDD_list = []
    for tmp in tmp_list:
        HDD_list.append(calcu_HDD(tmp))
    HDD_sum = sum(HDD_list)
    rwd = amount * max((HDD_sum - ini_price), 0)
    return rwd


if __name__ == "__main__":
    pass


