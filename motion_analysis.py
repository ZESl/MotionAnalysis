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

    df_result = pd.concat(df_list, axis=0, join='outer')
    df_result.to_csv(file_name)
    print('Concat all file done.')


# save all data (add user features)
def add_user(file_name):
    df_motion = pd.read_csv(file_name, encoding='gbk')
    df_motion["uid"] = df_motion["uid"].astype(str)
    df_user = pd.DataFrame(get_all_users(), columns=['uid', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)'])
    df_result = pd.merge(df_motion, df_user, on='uid')
    df_result.to_csv('user_' + file_name)


def analyze_event(df, event_type):
    df_t = df[df.event_type == event_type]
    # print(df_t.describe())


if __name__ == '__main__':

    filename = 'Result.csv'
    if not os.path.exists(filename):
        concat_all(filename)
        add_user(filename)
        
    # Analyze Event
    # i: event type (include 1,2,3)
    df_all = pd.read_csv(filename, encoding='gbk', index_col=0)
    for i in range(1, 4):
        analyze_event(df_all, i)
