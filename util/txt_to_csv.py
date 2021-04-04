import os
import pandas as pd
import numpy as np


# pid: person id        tid: trial id
# lc_x: left controller x axis
def convert_txt_csv(txt_path, csv_path, pid, tid):
    title = ["time", "lc_x", "lc_y", "lc_z", "rc_x", "rc_y", "rc_z", "lt_x", "lt_y", "lt_z", "rt_x", "rt_y", "rt_z"]

    with open(txt_path) as file:
        lines = file.readlines()
        df = pd.DataFrame(columns=title)
        for line in lines:
            line = line.strip("\n")
            string = line.split("  ")

            leftController = string[1].strip(" ")[16:-1].split(",")
            rightController = string[2][17:-1].split(",")
            leftTracker = string[3][13:-1].split(",")
            rightTracker = string[4][14:-1].split(",")

            lc_x = leftController[0].strip(" ")
            lc_y = leftController[1].strip(" ")
            lc_z = leftController[2].strip(" ")
            rc_x = rightController[0].strip(" ")
            rc_y = rightController[1].strip(" ")
            rc_z = rightController[2].strip(" ")
            lt_x = leftTracker[0].strip(" ")
            lt_y = leftTracker[1].strip(" ")
            lt_z = leftTracker[2].strip(" ")
            rt_x = rightTracker[0].strip(" ")
            rt_y = rightTracker[1].strip(" ")
            rt_z = rightTracker[2].strip(" ")

            # 假如有一个设备断连了，则这条数据作废
            if (lc_x == 0 and lc_y == 0 and lc_z == 0) or (rc_x == 0 and rc_y == 0 and rc_z == 0) or \
                    (lt_x == 0 and lt_y == 0 and lt_z == 0) or (rt_x == 0 and rt_y == 0 and rt_z == 0):
                continue

            # ["time", "lc_x", "lc_y", "lc_z", "rc_x", "rc_y", "rc_z", "lt_x", "lt_y", "lt_z", "rt_x", "rt_y", "rt_z"]
            data = [{"time": string[0],
                     "lc_x": lc_x,
                     "lc_y": lc_y,
                     "lc_z": lc_z,
                     "rc_x": rc_x,
                     "rc_y": rc_y,
                     "rc_z": rc_z,
                     "lt_x": lt_x,
                     "lt_y": lt_y,
                     "lt_z": lt_z,
                     "rt_x": rt_x,
                     "rt_y": rt_y,
                     "rt_z": rt_z}]
            df = df.append(data, ignore_index=True)
        # print(df)

        lcx = df.iloc[0, 1]
        rcx = df.iloc[0, 4]
        if float(lcx) > float(rcx):
            # 说明左右手反了
            df = df[["time", "rc_x", "rc_y", "rc_z", "lc_x", "lc_y", "lc_z", "lt_x", "lt_y", "lt_z", "rt_x", "rt_y",
                     "rt_z"]]

        ltx = df.iloc[0, 7]
        rtx = df.iloc[0, 10]
        if float(ltx) > float(rtx):
            # 说明左右脚反了
            df = df[["time", "lc_x", "lc_y", "lc_z", "rc_x", "rc_y", "rc_z", "rt_x", "rt_y", "rt_z", "lt_x", "lt_y",
                     "lt_z"]]
        df.to_csv(csv_path, header=title, index=False)


for txt_file in os.listdir("../data_txt"):
    # print(txt_file)
    csv_file = txt_file.split(".")[0] + ".csv"
    info = txt_file.split(".")[0].split("-")
    convert_txt_csv("../data_txt/" + txt_file, "../data_csv/" + csv_file, info[0], info[1])
