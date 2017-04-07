from AnnAnalyst import analysing
from AnnAnalyst import conmatrix
from AnnAnalyst import giveCats
from InterCompare import namelist
import csv

cats = giveCats()
tt = 150 * 55


def summarizing():
    overviewSum = {}
    nl = list(namelist())
    for name in nl:
        res = analysing(conmatrix(name))
        overviewSum.update({name: res})

    return overviewSum


def givePara(cat):
    para = [0, 0, 0, 0]

    ov = summarizing()
    for k in ov.values():
        # print(k)
        para[0] += k[cat]['tp']
        para[1] += k[cat]['fn']
        para[2] += k[cat]['fp']
        para[3] += k[cat]['tn']

    return para


def crsCat():
    cr = {}
    for c in cats:
        tp = givePara(c)[0]
        fn = givePara(c)[1]
        fp = givePara(c)[2]
        tn = givePara(c)[3]
        tt = tp + fn + fp + tn
        ea = ((fp + tn) * (tn + fn) + (tp + fp) * (tp + fn)) / (tt * tt)  # expected agreement

        cr.update({c: givePara(c)})
        if tp == 0 & fn == 0 & fp == 0:
            print(cr[c])
            cr[c].append(1)
            cr[c].append(1)
            cr[c].append(1)
            cr[c].append(1)
        else:
            cr[c].append(tp / (tp + fp))  # precision 4
            cr[c].append(tp / (tp + fn))  # recall 5
            cr[c].append(2 * cr[c][4] * cr[c][5] / (cr[c][4] + cr[c][5]))  # f1 6
            cr[c].append(((tp + tn) / tt - ea) / (1 - ea))  # cohen 7

    return cr

if __name__ == "__main__":
    heading = ['overall', 'precision', 'recall', 'f1', 'cohen']
    crs = crsCat()

    with open('overall.csv', 'w') as ed:
        ed_csv = csv.writer(ed)
        ed_csv.writerow(heading)
        for ct in cats:
            pa = []
            for i in range(4, 8):
                pa.append(crs[ct][i])
            pa.insert(0, ct)
            ed_csv.writerow(pa)
    ed.close()
