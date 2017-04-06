'''
this is to calculate the key indicators such as precision and recall given the sorted data and a specified Unikey
'''


import csv
from collections import Counter

user = 'cnin0770'
inputfile = 'ann_edited.csv'
outputfile = 'ind_cnin0770.csv'
tt = 150
raters = 55
cats = [
    'Education',
    'Entertainment',
    'Finance',
    'Health',
    'Hospitality',
    'Public administration',
    'Real estate',
    'Resources',
    'SciTech',
    'Social',
    'Sports',
    'Trade',
    'Transport',
    'Other',
    'Error'
]


def readmatrix(individual):
    gold = []
    pred = []

    crs = {}
    for cat in cats:
        crs[cat] = {
            'Education': 0,
            'Entertainment': 0,
            'Finance': 0,
            'Health': 0,
            'Hospitality': 0,
            'Public administration': 0,
            'Real estate': 0,
            'Resources': 0,
            'SciTech': 0,
            'Social': 0,
            'Sports': 0,
            'Trade': 0,
            'Transport': 0,
            'Other': 0,
            'Error': 0
        }
    # for cat in cats:
    #     for dog in cats:
    #         crs[cat].update({dog: 0})

    with open(inputfile, "r", encoding='utf-8', errors='ignore') as ann:
        ann_csv = csv.reader(ann)
        heading = next(ann_csv)
        col_no = heading.index(individual)

        for i in range(0, tt):
            row = next(ann_csv)
            gold.append(row[1])
            pred.append((row[col_no]))
            crs[row[1]][row[col_no]] += 1

        for row in cats:
            crs[row]['totalGold'] = 0
            crs[row]['totalPred'] = 0
            for col in cats:
                crs[row]['totalGold'] += crs[row][col]
                crs[row]['totalPred'] += crs[col][row]

    ann.close()
    return crs


def flissmatrix():
    flissM = []

    with open(inputfile, "r", encoding='utf-8', errors='ignore') as ann:
        ann_csv = csv.reader(ann)
        for row in ann_csv:
            rowed = row
            if rowed:
                rowed.pop(0)  # pop article names
                rowed.pop(0)  # pop GOLD
            flissM.append(Counter(rowed))

    ann.close()
    flissM.pop(0)  # pop heading

    res = []
    k = 0
    pi = 0
    pe = 0

    for mat in flissM:
        res.append([])
        for cat in cats:
            if cat in mat.keys():
                res[k].append(mat[cat])
            else:
                res[k].append(0)
        k += 1
    del res[-1]  # remove last empty line caused by res.append([])

    for i in range(len(res)):
        for j in range(len(res[i])):
            pi += (res[i][j] * res[i][j]) / ((raters - 1) * raters)

        pi -= 1 / (raters - 1)
    pi = pi / tt

    for i in range(len(res[0])):
        pj = 0
        for j in range(len(res)):
            pj += res[j][i] / (raters * tt)
        pe += pj * pj

    return (pi - pe) / (1 - pe)


def analysing(matrix):
    analyst = {}
    for cat in cats:
        analyst[cat] = {}

    for cow in cats:
        totalGold = matrix[cow]['totalGold']
        totalPred = matrix[cow]['totalPred']
        tp = matrix[cow][cow]
        fn = totalGold - tp
        fp = totalPred - tp
        tn = tt - totalGold - totalPred + tp

        # print(cow, tp, fn, fp, tn, tp+fn+fp+tn)

        analyst[cow]['tp'] = tp
        analyst[cow]['fn'] = fn
        analyst[cow]['fp'] = fp
        analyst[cow]['tn'] = tn

        if tp == 0 & fn == 0 & fp == 0:
            pass
        else:
            analyst[cow]['precision'] = tp / (tp + fp)
            analyst[cow]['recall'] = tp / (tp + fn)
            analyst[cow]['f1'] = (2 * analyst[cow]['precision'] * analyst[cow]['recall']) /\
                                 (analyst[cow]['precision'] + analyst[cow]['recall'])
            analyst[cow]['accuracy'] = (tp + tn) / tt
            analyst[cow]['marginalFalse'] = (tt - totalPred) * (tt - totalGold) / (tt * tt)
            analyst[cow]['marginalTrue'] = totalPred * totalGold / (tt * tt)
            analyst[cow]['expectedAgreement'] = analyst[cow]['marginalTrue'] + analyst[cow]['marginalFalse']
            analyst[cow]['cohensKappa'] = (analyst[cow]['accuracy'] - analyst[cow]['expectedAgreement']) /\
                                          (1 - analyst[cow]['expectedAgreement'])

    return analyst


def outputfun(res, outputf):
    toWrite = [[]]
    toWrite[0].append(user)
    for key in res['Education'].keys():
        toWrite[0].append(key)

    k = 1
    for cat in cats:
        toWrite.append([])
        toWrite[k].append(cat)
        for value in res[cat].values():
            toWrite[k].append(value)
        k += 1

    with open(outputf, 'w') as ed:
        ed_csv = csv.writer(ed)
        for l in toWrite:
            ed_csv.writerow(l)

    ed.close()
    return True


# def namelist():
#     with open(inputfile, "r", encoding='utf-8', errors='ignore') as ann:
#         ann_csv = csv.reader(ann)
#         names = next(ann_csv)
#     ann.close()
#     names.pop()
#     names.pop()
#     return names

if __name__ == "__main__":
    result = analysing(readmatrix(user))

    print('Fleiss\' kappa:', format(flissmatrix(), '3.2%'))

    print(outputfun(result, outputfile))
