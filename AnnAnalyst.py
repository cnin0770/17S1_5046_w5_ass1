'''
this is to calculate the key indicators such as precision and recall given the sorted data and a specified Unikey
'''


import csv

tt = 150
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

    with open('ann_edited.csv', "r", encoding='utf-8', errors='ignore') as ann:
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

    return crs


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

if __name__ == "__main__":
    user = 'cnin0770'
    result = analysing(readmatrix(user))

    print(result['Entertainment'])
