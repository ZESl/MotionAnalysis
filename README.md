# MotionAnalysis

FUNCTION
---
已完成：基于Unity开发VR游戏，逐帧获取Controller和Tracker的位置数据。
该仓库完成以下几个功能：
1. get_cut.py 通过对位置数据进行动作分割、特征提取。
2. get_VR_event.py 获取VR事件数据
3. get_user_feature.py 获取用户数据（待写）
4. apriori.py 数据关联规则学习（待写）


FILE FOLDER
---
data_event
存放VR事件数据

data_event&cut
存放用户的cut数据和其对应的VR事件

data_json data_txt data_xls
均存放用户在使用VR设备时骨骼关节点的位置数据，以不同的数据格式存储

data_user
存放用户特性数据

images
存放matplotlib画的各种图

util
各种工具文件
