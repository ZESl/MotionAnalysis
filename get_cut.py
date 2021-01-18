import xlrd
import numpy as np
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


def cut(filename):
    # 读取文件
    data = xlrd.open_workbook("data_xls/" + filename + ".xls")
    table = data.sheets()[0]

    # start time
    start_time = table.cell(1, 0).value

    # write to data_event&cut
    f = open('data_event&cut/' + filename + ".csv", 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['time stamp', 'passed time(seconds)', 'side', 'cut length', 'event type'])

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

    # 判断静止状态的阈值
    threshold = 0.02

    # 迭代所有的行
    row = 1
    for i in range(2, table.nrows):
        row += 1

        # 当前行与上一行的差
        cur_time = table.cell(row, 0).value
        lc_temp_x = float(table.cell(row, 1).value) - float(table.cell(row - 1, 1).value)
        lc_temp_y = float(table.cell(row, 2).value) - float(table.cell(row - 1, 2).value)
        lc_temp_z = float(table.cell(row, 3).value) - float(table.cell(row - 1, 3).value)
        rc_temp_x = float(table.cell(row, 4).value) - float(table.cell(row - 1, 4).value)
        rc_temp_y = float(table.cell(row, 5).value) - float(table.cell(row - 1, 5).value)
        rc_temp_z = float(table.cell(row, 6).value) - float(table.cell(row - 1, 6).value)

        passed_time = time_sub_ms(start_time, cur_time)

        # 左手
        if abs(lc_temp_x) >= threshold or abs(lc_temp_y) >= threshold or abs(lc_temp_z) >= threshold:
            l_x.append(float(table.cell(row, 1).value))
            l_y.append(float(table.cell(row, 2).value))
            l_z.append(float(table.cell(row, 3).value))
        else:
            if len(l_x) > 2:
                curve = curve_3d(l_x, l_y, l_z)
                if curve > 0.1:
                    left.append(curve)
                    event = get_event_by_time(all_event, passed_time)
                    print("----pass time:" + str(passed_time) + "----")
                    print("event type:" + str(event))
                    print("左手三维空间曲线长度：{:.4f}".format(curve))
                    csv_writer.writerow([cur_time, passed_time, 'left', curve, event])
            l_x = []
            l_y = []
            l_z = []

        # 右手
        if abs(rc_temp_x) >= threshold or abs(rc_temp_y) >= threshold or abs(rc_temp_z) >= threshold:
            r_x.append(float(table.cell(row, 4).value))
            r_y.append(float(table.cell(row, 5).value))
            r_z.append(float(table.cell(row, 6).value))
        else:
            if len(r_x) > 2:
                curve = curve_3d(r_x, r_y, r_z)
                if curve > 0.1:
                    right.append(curve)
                    event = get_event_by_time(all_event, passed_time)
                    print("----pass time:" + str(passed_time) + "----")
                    print("event type:" + str(event))
                    print("右手三维空间曲线长度：{:.4f}".format(curve))
                    csv_writer.writerow([cur_time, passed_time, 'right', curve, event])
            r_x = []
            r_y = []
            r_z = []

    f.close()

    # get average cut length
    sum_right = 0
    sum_left = 0
    for i in range(0, len(right)):
        sum_right += right[i]
    average_right = sum_right / len(right)

    for i in range(0, len(left)):
        sum_left += left[i]
    average_left = sum_left / len(left)

    print('右手平均：', average_right)
    print('左手平均：', average_left)


if __name__ == '__main__':
    for txt_file in os.listdir("data_xls"):
        # print(txt_file)
        file_name = txt_file.split(".")[0]
        cut(file_name)