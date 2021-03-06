# Dong Liu
# created : 2022/2/10 10:54


############ Ausgangsgößen(Prognose des Gewichts) aus Regressionsaufabe müssen zu Klassifikation wechseln
############ 100 datasets----> standard deviation ----> prediction(Prognose des Gewichts) corret or not



'''
RIGHT Xt=0， FALSE Xt=1

'''


import os
import sys
import math
import numpy as np


class ECDD_DETEKTION(object):
    def __init__(self):
        self.threshold = 0              #Lt
        self.count = 0
        self.pr = 0.0                           #P0t
        self.sd = 0.0                           #sigma Xt
        self.expf = 0.0                         #lambda
        self.z = 0.0                            #Zt
        self.sdz = 0.0                          #sigma Zt


    def ecdd(self, values, expf=0.2, warmUp=0):     # values--->List für Prognose des Gewicht, .tolist()
        """
        ECDD algorithm
        """
        self.expf = expf                        ### parameter λ(hier=0.2), how much weight is given to more recent data compared with older data

        result = list()                         ### list für conceptdrift Informationen(count, estimator,conceptdirft)
        if warmUp > 0:
            for i in range(warmUp):
                self.ecddStep(values[i])
                r = (self.count, self.z, 0)     ### nur zählen und berechnen, keine Conceptdrift Detektion von [0 - warmUp)
                result.append(r)
        else:
            for i in range(warmUp, len(values), 1): ##Detektion von warmUp bis zum Ende
                self.ecddStep(values[i])
                self.threshold=1.17+7.56*self.pr-21.24*self.pr**3+112.12*self.pr**5-987.23*self.pr**7
                ###control limit



                bound = self.pr + self.threshold * self.sdz
                dr = 1 if self.z > bound else 0     ##  0->no Conceptdrift, 1->confirm CD
                if dr==1:
                    result.append(self.count)
                else:
                    continue




        return result

    def ecddStep(self, val):
        """
        ECDD one step exponential forecast
        """
        self.count += 1
        self.pr = ((self.count-1) * self.pr) / (self.count) + val / (self.count)          # p0t
        self.sd = self.pr * (1.0 - self.pr)                     # sigma xt
        e = 1.0 - self.expf
        self.sdz = math.sqrt(self.sd * self.expf * (1.0 - e ** (2 * self.count)) / (2.0 - self.expf))
        self.z = e * self.z + self.expf * val



'''
Value (Xt（1/0）) als input
'''
