''' 
this is to format the raw data into sensible sheet, 
and to generate the GOLD class by most-selected categories
'''


import csv
from collections import Counter

lines = 8250
units = 150


def getfile():
    with open(infile, "r", encoding='utf-8', errors='ignore') as ann:
        ann_csv = csv.reader(ann)
        results = [[]]
        k = 0

        for i in range(0, units + 1):
            results.append([])
            for j in range(0, lines // units + 1):
                results[i].append('')

        for row in ann_csv:
            if row[0] != results[0][k // units]:
                results[0][k // units + 1] = row[0]

            if row[1] != results[k % units]:
                results[k % units + 1][0] = row[1]

            results[k % units + 1][k // units + 1] = row[2]
            k += 1
    ann.close()

    results[0].insert(1, 'GOLD')

    for k in range(1, units + 1):
        kCount = Counter(results[k])
        results[k].insert(1, kCount.most_common(1)[0][0])

    return results


def givefile(results):
    with open(outfile, 'w') as ed:
        ed_csv = csv.writer(ed)
        ed_csv.writerows(results)
    ed.close()
    return True

if __name__ == "__main__":
    outfile = 'ann_edited.csv'
    infile = '5046_w4_0328_annotations.csv'
    print(givefile(getfile()))
