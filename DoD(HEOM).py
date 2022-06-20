
############ Ausgangsgößen aus Regressionsaufabe müssen zu Klassifikation wechseln
############  mittelwert und standardabweichung

import numpy as np
from math import sqrt
import numpy as np
import time
import xlwt
import pymysql
import pandas as pd
import numpy as np
from numpy import *
#
# dataset = np.array([[2.7810836,2.550537003,0],                  ###features and labels
# 	                [1.465489372,2.362125076,0],
# 	                [3.396561688,4.400293529,1],
# 	                [1.38807019,1.850220317,0],
# 	                [3.06407232,3.005305973,1],
# 	                [7.627531214,2.759262235,1],
# 	                [5.332441248,2.088626775,0],
# 	                [6.922596716,1.77106367,1],
# 	                [8.675418651,-0.242068655,1],
# 	                [7.673756466,3.508563011,1]])
#

'''
get range_a
'''
conn = pymysql.connect(host="000000",
					   database="0000000",
					   user="00000",
					   password="00000000",
					   port=00000,
					   charset="000000")

cursor1 = conn.cursor()         # get the basic datasets

table = 'daten'
cursor1.execute("select ActPrsCavMax1,"       
                "ActInj1HtgTmp1Ave,ActFrcClpMax,ActPowTot,ActPrsPlstSpecMax,ActPrsCavMax2 "
                "from {table} WHERE SetTimMachDat= '16.03.2022'"
                "and SetTimMachTim >'09:23:00'and ActCntCyc>0 and ActCntCyc<200;".format(table=table))
cursor1.scroll(0, mode='absolute')
results1 = cursor1.fetchall()
dataset=np.array(results1)
range_a=np.max(dataset, axis = 0) - np.min(dataset, axis = 0) #[21.     5.844  5.54   8.    20.868 15.   ]



# calculate the Euclidean distance between two vectors
def heom( x,y, range_a):                                                        #x,y are arrays
    results_list = []
    zhl=0               
    nen=0
    for i in range(x.shape[0]):                                       #last clonum is label
                                                                        #label=1, doesnt match
        heom_a = np.abs(x[i][:-1] - y[i][:-1])/range_a
        #print(heom_a)
        d_heom=np.sqrt(np.sum(np.square(heom_a)))                # return to float(heom)
        if x[i][-1]==y[i][-1]:
            disagree=0
        else:
            disagree=1
        zhl += d_heom*disagree
        nen += d_heom
    dod=zhl/nen
    return dod





#
'''
result analyse for k=2
[0.         0.         0.59478616 1.         1.         0.26861329
 0.33463201 1.         0.47567042 0.        ]
 
 	2.  row                [1.465489372,2.362125076,0],
	3.  row                [3.396561688,4.400293529,1],
	4.  row                [1.38807019,1.850220317,0], 
	
 for 4.row dod=1: dataset[3][2]=!dataset[2][2] and dataset[2][2]=!dataset[1][2], disg=1, Zähler=Nenner
 
 
 
 	8.  row                [6.922596716,1.77106367,1],
	9.  row                [8.675418651,-0.242068655,1],
	10.  row               [7.673756466,3.508563011,1]
	
for 10.row dod=0: dataset[9][2]==dataset[8][2]and dataset[8][2]==dataset[7][2], disg=0, Zähler=0

so set bigger k value is better (avoid 1/0)
'''

'''

mittelwert und standardabweichung von dod
sodern due überder Zeitaufgezeichneten werte von DoD signifikant ansteigt, 
gilt ein concept drift als erkannt

'''

