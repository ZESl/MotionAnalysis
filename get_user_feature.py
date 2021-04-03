import csv
import pandas as pd


# return a dataframe given all features of all users
def get_all_users_all_features():
    with open('data_user/user.csv', 'r', encoding='utf-8') as csv_file:
        csv_file = csv.reader(csv_file)
        all_user_data = []
        flag = True
        for line in csv_file:
            # skip the first row
            if flag:
                flag = False
                continue

            # one piece of user data
            user_data = list()
            user_data.append(line[0])  # uid
            for i in range(6, len(line)):  # append other features
                user_data.append(line[i])

            # add the user data to all-list
            all_user_data.append(user_data)
    # todo modify the columns
    all_user_data_df = pd.DataFrame(all_user_data, columns=['uid', 'gender', 'age', 'height', 'weight',
                                                            'side', 'VR_exp', 'game_fre', 'sport_fre',
                                                            'difficulty', 'enjoyment', 'fatigue'])
    return all_user_data_df


# example featureList = ['uid', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)']
def get_all_user_feature_filtered(feature_list):
    df = get_all_users_all_features()
    return df[feature_list]


def get_user_by_id(all_user_data, uid):
    return all_user_data[uid - 1]


# if __name__ == '__main__':
#     print(get_user_by_id(get_all_users(), 1))
