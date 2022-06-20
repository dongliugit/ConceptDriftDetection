# Dong Liu
# created : 2022/4/11 14:30
import numpy as np
import openpyxl
import csv
import numpy as np
from numpy import *
import pandas as pd
import time
import matplotlib.pyplot as plt

PATH_cusum=input("Pfad hinzufügen, bei dem tatsächliche Forteilgewicht und Prognose abgelesen werden können")


def detect_cusum_oben(X,Y, M_oben=2.49, v=0.002):
    x = np.atleast_1d(X).astype('float64')
    y = np.atleast_1d(Y).astype('float64')
    M=np.zeros(x.size)
    taip = np.array(['positive', ])

    for i in range (0,len(x)):
        if i==0:
            M[i]=0+x[i]-y[i]-v
        else:
            M[i]=M[i-1]+x[i]-y[i]-v

        if M[i]>0:
            if M[i]-M_oben>0:
                taip=np.append(taip,i)
                M[i]=0
        else:
            M[i]=0
    return taip


def detect_cusum_unten(X,Y, M_unten=-2.49, v=-0.002):
    x = np.atleast_1d(X).astype('float64')
    y = np.atleast_1d(Y).astype('float64')
    M=np.zeros(x.size)
    tain = np.array(['negative', ])

    for i in range (0,len(x)):
        if i == 0:
            M[i] = 0 + x[i] - y[i] - v
        else:
            M[i]=M[i-1]+x[i]-y[i]-v

        if M[i]<0:
            if M[i]-M_unten<0:
                tain=np.append(tain,i)
                M[i]=0
        else:
            M[i]=0
    return tain

Gewciht_File = open('{PATH}'.format(PATH=PATH_cusum))
Gewicht_Reader = csv.reader(Gewciht_File,delimiter=';')
Gewicht_Data = list(Gewicht_Reader)

t_cusum=0
X_real=[]
X_predict=[]
X_count=[]

for i in range(1,len(Gewicht_Data) ):
    t_cusum+=1
    X_count.append(t_cusum)
    X_GEWICHT_real=float(Gewicht_Data[i][1])
    X_real.append(X_GEWICHT_real)
    X_GEWICHT_predict=float(Gewicht_Data[i][2])
    X_predict.append(X_GEWICHT_predict)


CD_unten=detect_cusum_unten(X_predict,X_real)

CD_OBEN=detect_cusum_oben(X_predict,X_real)



Deviation_axis=[]
for i in range(len(X_real)):
    deviation=(X_predict[i]-X_real[i])
    Deviation_axis.append(deviation)

CD_detekted_unten=[]
for i in range (1,len(CD_unten)):
    try:
        CD_detekted_unten.append(float(CD_unten[i]))
    except:
        print('no detekted')
CD_Y_unten = [0] * (len(CD_detekted_unten))

plt.scatter(CD_detekted_unten,CD_Y_unten, color='darkgray',marker='o' )

CD_detekted_oben=[]
for i in range (1,len(CD_OBEN)):
    try:
        CD_detekted_oben.append(float(CD_OBEN[i]))
    except:
        print('no detekted')
CD_Y_oben = [0] * (len(CD_detekted_oben))

plt.scatter(CD_detekted_oben,CD_Y_oben,color='brown',marker='o' )

'''
plot
'''
y_zeros=[0]*len(X_count)
plt.plot(X_count,y_zeros,color='red')
plt.axis([0,len(X_count),np.min(Deviation_axis),np.max(Deviation_axis)])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.plot(X_count,Deviation_axis)
plt.xlabel('Zyklen',fontsize=20)
plt.ylabel('Prognose - Real (Gewicht:g)',fontsize=20)
plt.text(100,0.10,"Grenzwert:2.49\nAkzeptable Drift:0.002",fontsize=20)
plt.show()
