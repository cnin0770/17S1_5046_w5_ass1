from AnnAnalyst import analysing
from AnnAnalyst import conmatrix
from AnnAnalyst import fleiss
import csv

heading = (
    'Unikey',
    'TruePostive',
    'FalseNegative',
    'FalsePostive',
    'TrueNegative',
    'Precision',
    'Recall',
    'F1 Score',
    'Accuracy',
    'MarginalFalse',
    'MarginalTrue',
    'ExpectedAgreement',
    'Cohen\'sKappa'
)

fle = ('Fleiss\' Kappa:', fleiss())


def namelist():
    with open('ann_edited.csv', "r", encoding='utf-8', errors='ignore') as ann:
        ann_csv = csv.reader(ann)
        names = next(ann_csv)
    ann.close()
    names.pop(0)
    names.pop(0)
    return names


def summarizing():
    overviewSum = {}
    nl = list(namelist())
    for name in nl:
        res = analysing(conmatrix(name))['overview']
        overviewSum.update({name: res})

    return overviewSum


def keylist():
    overviewsum = summarizing()
    return overviewsum['cnin0770'].keys()


def outf(fname):
    table = []
    kl = list(keylist())
    table.append(kl.insert(0, 'summary'))
    nl = list(namelist())
    summ = summarizing()

    for name in nl:
        line = []
        vs = list(summ[name].values())
        for value in vs:
            line.append(value)
        line.insert(0, name)
        table.append(line)

    table.pop(0)  # first is None, pop it

    with open(fname, 'w') as ed:
        ed_csv = csv.writer(ed)
        ed_csv.writerow(heading)
        for line in table:
            ed_csv.writerow(line)
        ed_csv.writerow(fle)

    ed.close()
    return True


if __name__ == "__main__":
    outfile = 'summarizing.csv'
    print(outf(outfile))
