import os
import pandas as pd
from get_user_feature import get_all_users


# save all motion data from folder:data_event
# + add uid trial
# - filter data from small cut lengths
def concat_all(file_name):
    df_list = []
    for file in os.listdir("data_event&cut"):
        df = pd.read_csv('data_event&cut/' + file, encoding='gbk', index_col=0)
        # df = df.set_index('time stamp')

        # define cut length filter condition
        mean_length = df["cut_length"].mean()
        min_length = df["cut_length"].min()
        sift_length = mean_length - min_length
        df = df[df.cut_length > sift_length]  # filter

        # resolve filename and add column to df
        uid = file.split('.')[0].split('-')[0]
        trial = file.split('.')[0].split('-')[1]
        df.insert(0, 'uid', uid)
        df.insert(1, 'trial', trial)

        # add to df_list
        df_list.append(df)

    df_motion = pd.concat(df_list, axis=0, join='outer')
    df_motion.to_csv(file_name)
    print('Concat all file done.')

    return df_motion


# save all data (add user features)
# filter some irrelevant features: eg. ['passed_time', 'name']
def add_user(df_motion, file_name):
    df_motion["uid"] = df_motion["uid"].astype(str)
    df_user = pd.DataFrame(get_all_users(), columns=['uid', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)'])
    df_result = pd.merge(df_motion, df_user, on='uid')
    print('add_user: Add user done.')

    drop_list = ['passed_time', 'name']
    df_result = df_result.drop(drop_list, axis=1)
    df_result.to_csv(file_name)
    print('add_user: Strip done.')
    return df_result


# get mean, min, max, ... data to form a dataset
def get_dataset(df, file_name):
    df_dataset = {
        "uid": [],
        "side": [],
        "event": [],
        "trial": [],
        "cut_mean": [],
        "cut_max": [],
        "cut_min": [],
        "cut_std": [],
        "cut_var": [],
        "speed_mean": [],
        "speed_max": [],
        "speed_min": [],
        "speed_std": [],
        "speed_var": [],
    }
    # todo modify range
    side_op = ['left', 'right']
    for uid in range(1, 4):  # uid: 1 2 3
        for event_type in range(1, 4):  # event_type: 1 2 3
            for trial in range(1, 3):  # trial: 1 2
                for side in side_op:  # side: 0 1
                    df_t = df[(df.event_type == event_type) & (df.uid == uid) & (df.trial == trial) & (df.side == side)]
                    df_dataset["uid"].append(uid)
                    df_dataset["side"].append(side)
                    df_dataset["event"].append(event_type)
                    df_dataset["trial"].append(trial)
                    df_dataset["cut_mean"].append(df_t["cut_length"].mean())
                    df_dataset["cut_min"].append(df_t["cut_length"].min())
                    df_dataset["cut_max"].append(df_t["cut_length"].max())
                    df_dataset["cut_std"].append(df_t["cut_length"].std())
                    df_dataset["cut_var"].append(df_t["cut_length"].var())
                    df_t = df_t[(df_t.speed > 0)]
                    df_dataset["speed_mean"].append(df_t["speed"].mean())
                    df_dataset["speed_min"].append(df_t["speed"].min())
                    df_dataset["speed_max"].append(df_t["speed"].max())
                    df_dataset["speed_std"].append(df_t["speed"].std())
                    df_dataset["speed_var"].append(df_t["speed"].var())
    df_dataset = pd.DataFrame(df_dataset)
    df_dataset.to_csv(file_name)
    print('get_dataset: Get dataset done.')
    df_dataset["uid"] = df_dataset["uid"].astype(str)
    df_user = pd.DataFrame(get_all_users(), columns=['uid', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)'])
    df_dataset = pd.merge(df_dataset, df_user, on='uid')
    print('get_dataset: Add user done.')
    return df_dataset


def categorize_cut_speed(df, file_name):
    # unfinished
    df_result = df
    df_result.to_csv(file_name)
    print('categorize_cut_speed: Categorize done.')
    return df_result


if __name__ == '__main__':
    # include all motion data
    filename = 'Dataset/Data_motion.csv'
    df_m = concat_all(filename)
    df_r = add_user(df_m, 'Dataset/Data_motion_user.csv')

    # only contains mean/min/max motion data
    df_m = pd.read_csv(filename, encoding='gbk')
    df_d = get_dataset(df_m, 'Dataset/Data_dataset_user.csv')

    # categorize_cut_speed(df_d, 'Dataset/Data_dataset_user(categorized).csv')
