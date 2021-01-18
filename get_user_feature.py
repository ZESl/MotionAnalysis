import csv


# unfinished
# feature = ['id', 'name', 'gender', 'age', 'height(cm)', 'weight(kg)']
def get_all_users():
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
    return all_user_data


def get_user_by_id(uid):
    all_user_data = get_all_users()
    return all_user_data[uid - 1]

# if __name__ == '__main__':
#     print(get_all_users())
#     print(get_user_by_id(1))
