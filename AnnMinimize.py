# not in use; integrated into AnnEditor

import csv
from collections import Counter

with open('ann_edited_nonCnin.csv', "r", encoding='utf-8', errors='ignore') as ann:
    ann_csv = csv.reader(ann)
    results = []
    results.append(['', 'most_common', 'cnin'])
    row_i = 1

    for row in ann_csv:
        results.append([])
        rowCounts = Counter(row)
        mostCommon = rowCounts.most_common(1)[0][0]

        results[row_i].append(row[0])
        results[row_i].append(mostCommon)
        row_i += 1

with open('ann_edited_min.csv', 'w') as ed:
    ed_csv = csv.writer(ed)
    ed_csv.writerows(results)