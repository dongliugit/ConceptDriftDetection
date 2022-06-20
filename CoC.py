# Dong Liu
# created : 2022/2/15 18:56
import numpy as np
from scipy.stats import t


def compute_histogram(X, n_bins):
    return np.array([np.histogram(X[:, i], bins=n_bins, density=False)[0] for i in range(X.shape[1])])
'''
return to histogram(X)==>  array ==> 
==> each colum contain ->probabilty of values, rows means->features

Histo(X)/(Y) =[            value1 v2 v3 v4 .... vm
                    f1      ...   .  .  .  .... ..    
                    f2      ...   .  .  .  .... ..
                    f3      ...   .  .  .  .... ..
                            ...   .  .  .  .... ..
                    fk      ...   .  .  .  .... ..   ]

'''

class CoC():
    def __init__(self, X,coc_Threshold):             # k(features) * m(samples) m-->user defined
        self.X=X
        self.n_bins = 0
        self.t= 0
        self.hist_baseline=0
        self.coc_Threshold=coc_Threshold

    def add_batch(self, Y):
        '''MUST be 2D '''
        self.n_bins = int(np.ceil(np.sqrt(Y.shape[0])))
        self.hist_baseline = compute_histogram(self.X, self.n_bins)

        self.t += 1

        hist=compute_histogram(Y,self.n_bins)
        corr= np.corrcoef(self.hist_baseline,hist)



        #need to select elements for CoC
        coc_array=np.array( [[corr[i,i+Y.shape[1]] for i in range (Y.shape[1])] ])
        CoC_value=np.sum(1/2-coc_array/2)/Y.shape[1]

        print(self.t,CoC_value)

        if CoC_value >self.coc_Threshold:

            print(self.t,"Drift detected, Adaption needed")

        self.X = Y

'''
always detect the newest 2 batches
'''



