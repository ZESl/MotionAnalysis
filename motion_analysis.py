import os
import pandas as pd
from get_user_feature import get_all_users
from util.draw import draw_scatter, draw_scatter_multi


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
def add_user(df_motion, file_name):
    df_motion["uid"] = df_motion["uid"].astype(str)
    df_user = pd.DataFrame(get_all_users(), columns=['uid', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)'])
    df_result = pd.merge(df_motion, df_user, on='uid')
    df_result.to_csv(file_name)
    return df_result


def strip_dataset(df_result, file_name):
    drop_list = ['passed_time', 'name']
    df_stripped = df_result
    df_stripped = df_stripped.drop(drop_list, axis=1)
    df_stripped.to_csv(file_name)
    return df_stripped


def analyze_event(df, uid, event_type):
    df_t = df[(df.event_type == event_type) & (df.uid == uid)]
    cut_list.append(df_t['cut_length'].mean())
    x_cut.append(str(uid) + '-' + str(event_type))


def analyze_trial(df, uid, event_type, trial):
    df_t = df[(df.event_type == event_type) & (df.uid == uid) & (df.trial == trial)]
    trial_list.append(df_t['cut_length'].mean())
    x_trial.append(str(event_type) + '-' + str(trial))
    print('uid:', uid, ' event_type:', event_type, ' trial:', trial, ' cut_length:', df_t['cut_length'].mean())


if __name__ == '__main__':

    # write to file
    filename = 'Data_motion.csv'
    if not os.path.exists(filename):
        df_m = concat_all(filename)
        df_r = add_user(df_m, 'Data_result.csv')
        df_s = strip_dataset(df_r, 'Data_stripped.csv')

    # Analyze Event
    df_all = pd.read_csv(filename, encoding='gbk')
    x_cut = []
    cut_list = []
    x_trial = []
    trial_list_all = []
    for i in range(1, 4):  # uid
        x_trial = []
        trial_list = []
        for j in range(1, 4):  # event_type
            analyze_event(df_all, i, j)

            # Analyze Trial
            for k in range(1, 3):  # trial
                analyze_trial(df_all, i, j, k)
        trial_list_all.append(trial_list)
        # draw_scatter(x_trial, trial_list, 'event-trial', 'cut-length')
    draw_scatter_multi(x_trial, trial_list_all, 'event-trial', 'cut-length')
    draw_scatter(x_cut, cut_list, 'uid-event', 'cut-length')
