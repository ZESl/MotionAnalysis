import matplotlib.pyplot as plt
import xlrd

# 读取文件
data = xlrd.open_workbook("../data_xls/2-1.xls")
table = data.sheets()[0]

# 打开画图窗口1，在三维空间中绘图
fig = plt.figure(1)
ax = fig.gca(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel("z")
ax.set_zlabel("y")
plt.title('Motion Track of Controllers and Trackers', fontsize=12)

# left controller
lc_x = list()
lc_y = list()
lc_z = list()
# right controller
rc_x = list()
rc_y = list()
rc_z = list()
# left tracker
lt_x = list()
lt_y = list()
lt_z = list()
# right tracker
rt_x = list()
rt_y = list()
rt_z = list()

for row in range(500, 700):
    lc_x.append(float(table.cell(row, 1).value))
    lc_y.append(float(table.cell(row, 2).value))
    lc_z.append(float(table.cell(row, 3).value))
    rc_x.append(float(table.cell(row, 4).value))
    rc_y.append(float(table.cell(row, 5).value))
    rc_z.append(float(table.cell(row, 6).value))
    lt_x.append(float(table.cell(row, 7).value))
    lt_y.append(float(table.cell(row, 8).value))
    lt_z.append(float(table.cell(row, 9).value))
    rt_x.append(float(table.cell(row, 10).value))
    rt_y.append(float(table.cell(row, 11).value))
    rt_z.append(float(table.cell(row, 12).value))

color_left = '#87CEEB'
color_right = '#FA8072'

# 散点图
ax.scatter3D(lc_x, lc_z, lc_y, c=color_left, cmap='Blues')  # 绘制散点图
ax.scatter3D(rc_x, rc_z, rc_y, c=color_right, cmap='Blues')  # 绘制散点图
ax.scatter3D(lt_x, lt_z, lt_y, c=color_left, cmap='Blues')  # 绘制散点图
ax.scatter3D(rt_x, rt_z, rt_y, c=color_right, cmap='Blues')  # 绘制散点图

# 将数组中的前两个点进行连线
# figure = ax.plot(lc_x, lc_z, lc_y, c=color_left, label='left controller')
# figure = ax.plot(rc_x, rc_z, rc_y, c=color_right, label='right controller')
# figure = ax.plot(lt_x, lt_z, lt_y, c='r', label='left tracker')
# figure = ax.plot(rt_x, rt_z, rt_y, c='g', label='right tracker')

# 标记散点
ax.text(-0.1, 0.1, 1.5, "Left Controller")
ax.text(0.4, 0.1, 1.5, "Right Controller")
ax.text(lt_x[0] - 0.16, lt_z[0], lt_y[0] + 0.1, "Left Tracker")
ax.text(rt_x[0] - 0.16, rt_z[0], rt_y[0] + 0.1, "Right Tracker")

# plt.text("Right Controller")
plt.savefig("../images/MotionTrack.png")
plt.show()
