import csv

with open('5046_w4_0328_annotations.csv', "r", encoding='utf-8', errors='ignore') as ann:
    ann_csv = csv.reader(ann)
    results = [[]]
    k = 0

    for i in range(0, 151):
        results.append([])
        for j in range(0, 58):
            results[i].append('')

    for row in ann_csv:
        if row[0] != results[0][k // 150]:
            results[0][k // 150 + 1] = row[0]

        if row[1] != results[k % 150]:
            results[k % 150 + 1][0] = row[1]

        results[k % 150 + 1][k // 150 + 1] = row[2]
        k += 1

    # for s in results:
    #     print(len(s))
    #
    # print(len(results))


with open('ann_edited.csv', 'w') as ed:
    ed_csv = csv.writer(ed)
    ed_csv.writerows(results)

