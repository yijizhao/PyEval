__author__ = 'chris'

from pandas import DataFrame


class Evaluator:

    def __init__(self, m, inf):
        self.m = m
        self.inf = inf
        self.qd = self.rn_matrix(m)

    def frame_ord(self, data, r, c):
        return DataFrame(data, index=r, columns=c)

    def frame_mat(self, data, c):
        return DataFrame(data, columns=c)

    def rn_matrix(self, m):
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

    def conf_matrix(self, i):
        tp = self.qd[i][0]
        fp = self.qd[i][1]
        fn = self.inf[i] - self.qd[i][0]
        tn = self.inf['tot'] - tp - fp - fn
        return {'tp': tp,
                'fp': fp,
                'fn': fn,
                'tn': tn}

    def precision(self, i):
        m = self.conf_matrix(i)
        return m['tp'] / (m['tp'] + m['fp'])

    def recall(self, i):
        m = self.conf_matrix(i)
        return m['tp'] / (m['tp'] + m['fn'])

    def f_measure(self, beta, i):
        P, R = self.precision(i), self.recall(i)
        return ((beta**2+1)*P*R)/(beta**2*P+R)

    def accuracy(self, i):
        m = self.conf_matrix(i)
        return (m['tp'] + m['tn']) / (m['tp'] + m['tn'] + m['fp'] + m['fn'])

    def qRank(self, i, k):
        ii, qr = self.m[int(i.replace('q', ''))-1], []
        r, relv, ri = 0, 0, 1.00/float(self.inf[i])
        for x in range(0, k):
            rsw = ''
            if ii[x] is 'R':
                r += ri; relv += 1; rsw = 'X'
            qr.append([x+1, rsw, r, relv/float(x+1)])
        return qr

    def MAP(self, k):
        tl = []
        for i in range(0, len(self.m)):
            m, tot, c = self.qRank('q'+str(i+1), k), 0, 0
            for j in range(0, len(m)):
                if m[j][1] is 'X':
                    tot += m[j][3]; c += 1
            tl.append(tot/c)
        return sum(tl)/len(self.m)

    def kMeasure(self, m2):
        m, rr, nn, rn, nr = self.m, 0, 0, 0, 0
        for i in range(0, len(self.m)):
            for j in range(0, len(self.m[i])):
                if m[i][j] is 'R' and m2[i][j] is 'R':
                    rr += 1
                elif m[i][j] is 'N' and m2[i][j] is 'N':
                    nn += 1
                elif m[i][j] is 'R' and m2[i][j] is 'N':
                    rn += 1
                elif m[i][j] is 'N' and m2[i][j] is 'R':
                    nr += 1
        return {'RR': rr, 'NN': nn, 'RN': rn, 'NR': nr}

    def Kappa(self, m2):
        km = self.kMeasure(m2)
        #P(A)
        #P(E)
        #Kappa = P(A) - P(E) / 1 - P(E)

#-------------------------------------------------------------
#initial annotator
M  = [['R', 'N', 'R', 'N', 'R', 'R', 'N', 'N', 'R', 'N'],  # q1
      ['R', 'R', 'N', 'N', 'R', 'N', 'N', 'R', 'N', 'N'],  # q2
      ['N', 'R', 'R', 'R', 'R', 'N', 'N', 'N', 'R', 'N'],  # q3
      ['R', 'N', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N']]  # q4
#second annotator
M2 = [['R', 'R', 'R', 'R', 'R', 'R', 'N', 'N', 'N', 'N'],  # q1
      ['R', 'R', 'R', 'N', 'R', 'N', 'N', 'N', 'N', 'N'],  # q2
      ['N', 'R', 'R', 'R', 'R', 'N', 'N', 'N', 'R', 'N'],  # q3
      ['R', 'N', 'R', 'N', 'R', 'N', 'N', 'N', 'N', 'N']]  # q4
#general information
inf = {'tot': 250, 'q1': 10, 'q2': 12, 'q3': 15, 'q4': 8}

ev = Evaluator(M, inf)
q = 'q1'
#print ev.conf_matrix(q)
#print ev.precision(q)
#print ev.recall(q)
#print ev.f_measure(1.0, q)
#print ev.accuracy(q)
#print ev.frame_mat(ev.qRank(q), ['rank', 'R', 'P'])
#print ev.MAP(10)
print ev.kMeasure(M2)
