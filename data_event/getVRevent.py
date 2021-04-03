import json
import pandas as pd

with open('D:/PyCharm/MotionAnalysis/data_event/NormalStandard.json', 'r') as f:
    data = json.load(f)
notes = data['_notes']
tins = []
pre = 0
for note in notes:
    # print(note.keys())
    t = note['_time']
    event = 0
    if (note['_lineIndex'] == 1 and note['_type'] == 0) or (note['_lineIndex'] == 2 and note['_type'] == 1):
        event = 1
    elif (note['_lineIndex'] == 0 and note['_type'] == 0) or (note['_lineIndex'] == 3 and note['_type'] == 1):
        event = 2
    elif (note['_lineIndex'] == 2 and note['_type'] == 0) or (note['_lineIndex'] == 1 and note['_type'] == 1):
        event = 3
    elif (note['_lineIndex'] == 3 and note['_type'] == 0) or (note['_lineIndex'] == 0 and note['_type'] == 1):
        event = 4

    if t != pre:
        tins.append([t * 60 / 108, event])
        pre = t
    else:
        tins.pop()
        event = 5
        tins.append([t * 60 / 108, event])
        pre = t

print(tins)
dataframe = pd.DataFrame(tins)
dataframe.to_csv('VRevent.csv', header=None, index=False)