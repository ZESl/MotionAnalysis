import pandas as pd
import numpy as np


# 通过四分位把三个运动特征映射到为 0 1 2 3
def map_values_quarter(df_t, index, q3, q2, q1):
    dff = df_t.copy()  # dataframe拷贝不能直接赋值 需要用copy()函数
    for row in range(dff.shape[0]):
        value = float(dff.loc[row, index])
        if value < q1:
            dff.loc[row, index] = 0
        elif q1 <= value < q2:
            dff.loc[row, index] = 1
        elif q2 <= value < q3:
            dff.loc[row, index] = 2
        else:
            dff.loc[row, index] = 3
    return dff


def map_values_half(df_t, index, q2):
    dff = df_t.copy()
    for row in range(dff.shape[0]):
        value = float(dff.loc[row, index])
        if value < q2:
            dff.loc[row, index] = False
        else:
            dff.loc[row, index] = True
    return dff


if __name__ == '__main__':
    df = pd.read_csv("../Dataset/Data_dataset.csv", index_col=0)

    cut_q3 = np.percentile(df.dropna()["cut_mean"], 75)
    cut_q2 = np.percentile(df.dropna()["cut_mean"], 50)
    cut_q1 = np.percentile(df.dropna()["cut_mean"], 25)
    print(cut_q3, cut_q2, cut_q1)
    df_1 = map_values_quarter(df, "cut_mean", cut_q3, cut_q2, cut_q1)
    df_2 = map_values_half(df, "cut_mean", cut_q2)

    speed_q3 = np.percentile(df.dropna()["speed_mean"], 75)
    speed_q2 = np.percentile(df.dropna()["speed_mean"], 50)
    speed_q1 = np.percentile(df.dropna()["speed_mean"], 25)
    print(speed_q3, speed_q2, speed_q1)
    df_1 = map_values_quarter(df_1, "speed_mean", speed_q3, speed_q2, speed_q1)
    df_2 = map_values_half(df_2, "speed_mean", speed_q2)

    space_q3 = np.percentile(df.dropna()["space_mean"], 75)
    space_q2 = np.percentile(df.dropna()["space_mean"], 50)
    space_q1 = np.percentile(df.dropna()["space_mean"], 25)
    print(space_q3, space_q2, space_q1)
    df_1 = map_values_quarter(df_1, "space_mean", space_q3, space_q2, space_q1)
    df_2 = map_values_half(df_2, "space_mean", space_q2)

    df_1 = df_1[["side", "event", "trial",
                 "gender", "age", "height", "weight", "fre_side", "VR_exp", "game_fre", "sport_fre",
                 "cut_mean", "speed_mean", "space_mean"]]

    df_1 = df_1[df_1["event"] != 4]
    df_1.to_csv("../Dataset/RIPPER_quarter.csv", encoding='gbk')

    df_2 = df_2[["side", "event", "trial",
                 "gender", "age", "height", "weight", "fre_side", "VR_exp", "game_fre", "sport_fre",
                 "cut_mean", "speed_mean", "space_mean"]]
    df_2 = df_2[df_2["event"] != 4]
    df_2.to_csv("../Dataset/RIPPER_half.csv", encoding='gbk')
