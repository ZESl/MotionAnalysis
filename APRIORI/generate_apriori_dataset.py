import pandas as pd
import numpy as np

if __name__ == '__main__':
    df = pd.read_csv("../Dataset/RIPPER_quarter.csv", index_col=0)
    for row in range(df.shape[0]):
        for col in range(len(df.columns)):
            df.iloc[row, col] = df.columns.tolist()[col] + str(df.iloc[row, col])
    df = df[["side", "event", "trial",
             "gender", "age", "height", "weight", "VR_exp", "game_fre", "sport_fre",
             "difficulty", "enjoyment", "fatigue", "personality",
             "cut_mean", "speed_mean", "space_mean"]]
    df.to_csv("../Dataset/APRIORI.csv", encoding='gbk')
