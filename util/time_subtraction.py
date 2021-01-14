# perform time2-time1
# input time format: 2020.12.28 16:27:45
# output result format: xxx(seconds)


def time_sub(time1, time2):
    time1_h_m_s = get_h_m_s(time1)
    time2_h_m_s = get_h_m_s(time2)
    seconds = (time2_h_m_s[0] - time1_h_m_s[0]) * 3600 + (time2_h_m_s[1] - time1_h_m_s[1]) * 60 + (
            time2_h_m_s[2] - time1_h_m_s[2])
    return seconds


def get_h_m_s(time):
    time = time.split(" ")[1]
    # print(time)
    time_h_m_s = list()
    time_h_m_s.append(int(time.split(":")[0]))  # hour
    time_h_m_s.append(int(time.split(":")[1]))  # minute
    time_h_m_s.append(int(time.split(":")[2]))  # second
    return time_h_m_s
