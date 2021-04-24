import pandas as pd
import numpy as np

if __name__ == '__main__':
    df = pd.read_csv("../Dataset/RIPPER_spearman_half.csv")
    for row in range(df.shape[0]):
        for col in range(len(df.columns)):
            df.iloc[row, col] = df.columns.tolist()[col] + str(df.iloc[row, col])
    df.to_csv("../Dataset/APRIORI.csv", encoding='gbk')
