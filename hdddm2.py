# Dong Liu
# created : 2022/2/14 0:03
# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import t




def compute_histogram(X, n_bins):
    return np.array([np.histogram(X[:, i], bins=n_bins, density=False)[0] for i in range(X.shape[1])])

'''
density=False       the result will contain the number of samples in each bin
return to probabilty of values of each feature(colum)   (see onenote)
X convert to P, (unten) each colum contain ->probabilty of values, rows means->features
'''

def compute_hellinger_dist(P, Q):
    return np.mean(
        [np.sqrt(np.sum(np.square(np.sqrt(P[i, :] / np.sum(P[i, :])) - np.sqrt(Q[i, :] / np.sum(Q[i, :]))))) for i in
         range(P.shape[0])])

'''
mean----> cardinality==P.shape[0](number of feature)
'''
# Hellinger Distance Drift Detection Method
class HDDDM():                                      #X UND Y gleiche Größe (Dimension)
    def __init__(self, X, gamma=1.):


        self.gamma = gamma
        self.n_bins = 0

        # Initialization
        self.X_baseline = X


        self.dist_old = 0.
        self.epsilons = []
        self.t_denom = 0
        self.t_watch=0
        self.drift = False
    def add_batch(self, Y):
        self.t_denom += 1
        self.t_watch += 1
        self.n_bins = int(np.floor(np.sqrt(Y.shape[0])))   # it defines the number of equal-width bins in the given range


        self.hist_baseline = compute_histogram(self.X_baseline, self.n_bins)

        # Compute histogram and the Hellinger distance to the baseline histogram
        hist = compute_histogram(Y, self.n_bins)
        dist = compute_hellinger_dist(self.hist_baseline, hist)
        eps = dist - self.dist_old
        self.dist_old= dist
        if self.t_denom>1:
            self.epsilons.append(eps)
            print(self.epsilons)
            if self.t_denom>2   :
                epsilon_hat = ((1. / (self.t_denom-2))) * np.sum(np.abs(self.epsilons[:-1]))
                sigma_hat = np.sqrt(np.sum(np.square(np.abs(self.epsilons[:-1]) - epsilon_hat)) / (self.t_denom-2))
                beta = epsilon_hat + self.gamma * sigma_hat
                self.drift = np.abs(eps) > beta
            else:
                self.drift = False
        else:
            self.drift = False

        if self.drift == True:

            print(self.t_watch)
            self.t_denom = 0
            self.epsilons = []
            self.X_baseline = Y
            self.dist_old = 0.
            self.drift = False
        else:
            self.X_baseline = np.vstack((self.X_baseline, Y))



'''
gamma 可手动调整，决定beta这个threshold
至少需要三组batch， 计算出1,2 batch的hellinger distance，然后计算出（1verstack2），3的hellinger distance，然后比较
建议如下
Y包含5（可调）组数据，X要是100-105正常的数据
100-110为正常数据
detektion daten每加入5个就add_batch一次,只需要features的几列
'''

