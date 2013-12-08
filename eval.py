__author__ = 'chris'

from pandas import DataFrame


class Evaluator:

    def __init__(self, m, inf):
        self.inf = inf
        self.qd = self.rn_matrix(m, inf)

    def frame_ord(self, data, r, c):
        return DataFrame(data, index=r, columns=c)

    def rn_matrix(self, m, inf):
        qd = {}
        for i in range(0, len(m)):
            rel, nrel = 0.0, 0.0
            for j in range(0, len(m[i])):
                if m[i][j] is 'R':
                    rel += 1
                else:
                    nrel += 1
            qd['q'+str(i+1)] = (rel, nrel)
        return qd

    def precision(self):
        qd = self.qd
        for q, t in qd.items():
            qd[q] = t[0] / (t[1] + t[0])
        return qd

    def recall(self):
        qd = self.qd
        for q, t in qd.items():
            qd[q] = t[0] / self.inf[q]
        return qd

    def conf_matrix(self, i):
        return [[self.qd[i][0], self.qd[i][1]],
                [self.inf[i]-self.qd[i][0], self.inf[i]-self.qd[i][1]]]


M = [['R', 'N', 'R', 'N', 'R', 'R', 'N', 'N', 'R', 'N'],
     ['R', 'R', 'N', 'N', 'R', 'N', 'N', 'R', 'N', 'N'],
     ['N', 'R', 'R', 'R', 'R', 'N', 'N', 'N', 'R', 'N'],
     ['R', 'N', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N']]
inf = {'tot': 250, 'q1': 10, 'q2': 12, 'q3': 15, 'q4': 8}
ev = Evaluator(M, inf)
print ev.frame_ord(ev.conf_matrix('q3'), ['sel', 'nosel'], ['cor', 'nocor'])
