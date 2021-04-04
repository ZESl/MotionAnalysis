# import xlrd
import numpy as np
import pandas as pd
import csv
import os
from util.time_subtraction import time_sub_ms
from get_VR_event import get_all_event, get_event_by_time


# 三维空间曲线，采用参数形式
def curve_3d(x, y, z):
    area_list = []  # 存储每一微小步长的曲线长度

    for i in range(1, len(x)):
        # 计算每一微小步长的曲线长度，dx = x_{i}-x{i-1}，索引从1开始
        dl_i = np.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2 + (z[i] - z[i - 1]) ** 2)
        # 将计算结果存储起来
        area_list.append(dl_i)

    area = sum(area_list)  # 求和计算曲线在t:[0,2*pi]的长度

    if area > 0.1:
        return area
    else:
        return 0


# 动作分割，并找出相对应的VR事件，写入文件 data_event&cut/xxx.csv
# 包括：time stamp,passed time(seconds),side,cut length,event type
def cut(filename):
    # 读取文件
    # with open("data_csv/" + filename + ".csv")as f_in:

    # write to data_event&cut
    f = open('data_event&cut/raw/' + filename + ".csv", 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['timestamp', 'passed_time', 'side', 'cut_length', 'time', 'speed', 'event_type'])

    # read
    df = pd.read_csv("data_csv/" + filename + ".csv")
    # f_csv = csv.reader(f_in)

    # start time
    start_time = df.iloc[0, 0]

    # event
    all_event = get_all_event()

    # 初始左右手动作幅度集合
    right = []
    left = []

    # 存放长动作
    r_x = []
    r_y = []
    r_z = []
    l_x = []
    l_y = []
    l_z = []

    # 存放时间
    l_t = []
    r_t = []

    # 判断静止状态的阈值
    threshold = 0.02
    # 迭代所有的行
    for row in range(1, df.shape[0]):
        # 当前行与上一行的差
        cur_time = df.iloc[row, 0]
        lc_temp_x = float(df.iloc[row, 1]) - float(df.iloc[row - 1, 1])
        lc_temp_y = float(df.iloc[row, 2]) - float(df.iloc[row - 1, 2])
        lc_temp_z = float(df.iloc[row, 3]) - float(df.iloc[row - 1, 3])
        rc_temp_x = float(df.iloc[row, 4]) - float(df.iloc[row - 1, 4])
        rc_temp_y = float(df.iloc[row, 5]) - float(df.iloc[row - 1, 5])
        rc_temp_z = float(df.iloc[row, 6]) - float(df.iloc[row - 1, 6])

        passed_time = time_sub_ms(start_time, cur_time)

        # 左右手分开计算
        # 左手
        # if abs(lc_temp_x) >= threshold or abs(lc_temp_y) >= threshold or abs(lc_temp_z) >= threshold:
        if abs(lc_temp_x) + abs(lc_temp_y) + abs(lc_temp_z) >= threshold:
            l_t.append(cur_time)
            l_x.append(float(df.iloc[row, 1]))
            l_y.append(float(df.iloc[row, 2]))
            l_z.append(float(df.iloc[row, 3]))
        else:
            if len(l_x) > 2:
                curve = curve_3d(l_x, l_y, l_z)
                if curve > 0.1:
                    left.append(curve)
                    event = get_event_by_time(all_event, passed_time)
                    time = time_sub_ms(l_t[0], cur_time)
                    speed = float(curve / time) if time > 0 else -1  # unit: m/s
                    # print("----pass time:" + str(passed_time) + "----")
                    # print("event type:" + str(event))
                    # print("左手三维空间曲线长度：{:.4f}".format(curve))
                    csv_writer.writerow([cur_time, passed_time, 'left', curve, time, speed, event])
            l_x = []
            l_y = []
            l_z = []
            l_t = []

        # 右手
        # if abs(rc_temp_x) >= threshold or abs(rc_temp_y) >= threshold or abs(rc_temp_z) >= threshold:
        if abs(rc_temp_x) + abs(rc_temp_y) + abs(rc_temp_z) >= threshold:
            r_t.append(cur_time)
            r_x.append(float(df.iloc[row, 4]))
            r_y.append(float(df.iloc[row, 5]))
            r_z.append(float(df.iloc[row, 6]))
        else:
            if len(r_x) > 2:
                curve = curve_3d(r_x, r_y, r_z)
                if curve > 0.1:
                    right.append(curve)
                    event = get_event_by_time(all_event, passed_time)
                    time = time_sub_ms(r_t[0], cur_time)
                    speed = float(curve / time) if time > 0 else -1  # unit: m/s
                    # print("----pass time:" + str(passed_time) + "----")
                    # print("event type:" + str(event))
                    # print("右手三维空间曲线长度：{:.4f}".format(curve))
                    csv_writer.writerow([cur_time, passed_time, 'right', curve, time, speed, event])
            r_x = []
            r_y = []
            r_z = []
            r_t = []

    f.close()

    df = pd.read_csv('data_event&cut/raw/' + filename + ".csv", encoding='gbk', index_col=0)
    print(df.describe())

    # define cut length filter condition
    max_sift = np.percentile(df["cut_length"], 75)
    min_sift = np.percentile(df["cut_length"], 25)
    print('sift range:', max_sift, min_sift)

    df = df[(df.cut_length <= max_sift)]  # filter
    df = df[(df.cut_length >= min_sift)]  # filter

    df_left = df[(df.side == 'left')]
    df_right = df[(df.side == 'right')]
    print('右手平均：', df_left["cut_length"].mean())
    print('左手平均：', df_right["cut_length"].mean())
    df.to_csv('data_event&cut/sifted/' + filename + ".csv")


# Tracker位移
# 按max-min来算矩形面积
def move(filename):
    # 读取文件
    df = pd.read_csv("data_csv/" + filename + ".csv")
    df.head()
    x_max = df["lt_x"].max() if df["lt_x"].max() > df["rt_x"].max() else df["rt_x"].max()
    x_min = df["lt_x"].min() if df["lt_x"].min() < df["rt_x"].min() else df["rt_x"].min()
    y_max = df["lt_y"].max() if df["lt_y"].max() > df["rt_y"].max() else df["rt_y"].max()
    y_min = df["lt_y"].min() if df["lt_y"].min() < df["rt_y"].min() else df["rt_y"].min()
    square = (x_max - x_min) * (y_max - y_min)
    print(square)


if __name__ == '__main__':
    for txt_file in os.listdir("data_csv"):
        print('--- ' + txt_file + ' ---')
        file_name = txt_file.split(".")[0]
        cut(file_name)
        move(file_name)
