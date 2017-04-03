'''
this is to calculate the key indicators such as precision and recall given the sorted data and a specified Unikey
'''


import csv
from collections import Counter

with open('ann_edited_min.csv', "r", encoding='utf-8', errors='ignore') as ann:
    ann_csv = csv.reader(ann)
    gold = []
    predicted = []

    for row in ann_csv:
        gold.append(row[1])
        predicted.append(row[2])

    goldCounts = Counter(gold)
    goldCounts = sorted(zip(goldCounts.keys(), goldCounts.values()))
    predictedCounts = Counter(predicted)
    predictedCounts = sorted(zip(predictedCounts.keys(), predictedCounts.values()))
    pdCounts = {}

    print(goldCounts)
    print(predictedCounts)

    # for k in goldCounts:
    #     pdCounts

# with open('indi_analysis.csv', 'w') as ed:
#     ed_csv = csv.writer(ed)
#     ed_csv.writerows(results)