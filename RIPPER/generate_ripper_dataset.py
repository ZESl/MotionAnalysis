import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 通过四分位把三个运动特征映射到为 0 1 2 3
def map_values(dff, index, q3, q2, q1):
    for row in range(dff.shape[0]):
        value = float(dff.loc[row, index])
        # print(value)
        if value < q1:
            dff.loc[row, index] = 0
        elif q1 <= value < q2:
            dff.loc[row, index] = 1
        elif q2 <= value < q3:
            dff.loc[row, index] = 2
        else:
            dff.loc[row, index] = 3
    return dff


if __name__ == '__main__':
    df = pd.read_csv("../Dataset/Data_dataset.csv")

    cut_q3 = np.percentile(df.dropna()["cut_mean"], 75)
    cut_q2 = np.percentile(df.dropna()["cut_mean"], 50)
    cut_q1 = np.percentile(df.dropna()["cut_mean"], 25)
    print(cut_q3, cut_q2, cut_q1)
    df = map_values(df, "cut_mean", cut_q3, cut_q2, cut_q1)

    speed_q3 = np.percentile(df.dropna()["speed_mean"], 75)
    speed_q2 = np.percentile(df.dropna()["speed_mean"], 50)
    speed_q1 = np.percentile(df.dropna()["speed_mean"], 25)
    print(speed_q3, speed_q2, speed_q1)
    df = map_values(df, "speed_mean", speed_q3, speed_q2, speed_q1)

    space_q3 = np.percentile(df.dropna()["space_mean"], 75)
    space_q2 = np.percentile(df.dropna()["space_mean"], 50)
    space_q1 = np.percentile(df.dropna()["space_mean"], 25)
    print(space_q3, space_q2, space_q1)
    df = map_values(df, "space_mean", space_q3, space_q2, space_q1)

    df = df[["side", "event", "trial",
             "gender", "age", "height", "weight", "fre_side", "VR_exp", "game_fre", "sport_fre",
             "cut_mean", "speed_mean", "space_mean"]]
    df.to_csv("../Dataset/RIPPER.csv", encoding='gbk')
