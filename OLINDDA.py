
from sklearn.cluster import KMeans
import numpy as np
'''
X-->lerning datasets(normal concept)
Y------>single new dataset

DATASETS=Olidda(X,5,3,4,3,10)
DATENSETS.add_newdata(Y)
DATENSETS.candidaten_cluster()

'''
class Olidda():
    def __init__(self,X,k,k_cluster,n_exin,n_excl,short_term_memory):
        '''
        :param X: array-like      for normal concept
        :param k: k means algorithmus for normal concept,user defined, updated after Model-adaption.no need to change here
        :param k_cluster: k means algorithmus for unknow datasets, user defined     (4) defined with n_excl and short_term_memory
        :param n_exin: number of examples per valid cluster in normal concept, user defined       (recommend 30)
        :param n_excl: number of examples per valid cluster in unknow datasets, user defined      (recommend 5)
        :param short_term_memory:  number in unknow dataset trigger to analyse, user defined        (20)
        '''

        self.X=X
        self.k=k
        self.k_cluster=k_cluster
        self.n_exin=n_exin
        self.n_excl = n_excl
        self.short_term_memory=short_term_memory
        self.kmeans = 0
        self.unknow=np.empty((0,X.shape[1]))                                       #empty array for unknow
        self.t_Y=0


    def add_newdata(self,Y):                        # new data(one data) and decide weather normal or unknow
        '''2D array np.array( [[]] )'''
        self.t_Y+=1
        self.detect_k()


        self.kmeans = KMeans(n_clusters=self.k, random_state=0).fit(self.X)        #k means algorithmus fitX

        self.Y=Y
        cluster_new=self.kmeans.predict(self.Y)                          # cluster label for new data
        distance_new=np.sqrt(np.sum((self.kmeans.transform(self.Y) ** 2), axis=1))      # distance between nearst centroid

        '''max distance for this cluster'''
        a=self.kmeans.transform(self.X)[np.where(self.kmeans.labels_==cluster_new)]      #array
        if a.shape[0]<self.n_exin:
            self.unknow=np.append(self.unknow,Y,axis=0)
        else:

            max_distance = np.max(np.sqrt(np.sum((a ** 2), axis=1)))

            if distance_new < max_distance:
                self.X = np.vstack((self.X, Y))
                print("normal concept",self.t_Y)
            else:
                self.unknow=np.append(self.unknow,Y,axis=0)

    '''the number of examples per cluster(normal concept) n_exin, make sure k always pass to initial concept'''
    def detect_k(self):
        k_need=self.k
        X_new=np.empty((0,self.X.shape[1]))
        self.kmeans = KMeans(n_clusters=self.k, random_state=0).fit(self.X)
        for m in range(self.k):
            a=self.kmeans.transform(self.X)[np.where(self.kmeans.labels_ == m)]         #array
            n_exin_test=a.shape[0]
            if n_exin_test > self.n_exin:
                for i in range(self.X.shape[0]):
                    if self.kmeans.labels_[i] == m:
                        X_new=np.append(X_new, [self.X[i]], axis=0)


            else:
                k_need-=1
                continue
        self.k=k_need
        self.X=X_new


    '''if k_cluster fit unknow datasets'''
    def detect_k_cluster(self):
        self.k_cluster=self.unknow.shape[0]//self.n_excl
        return  self.k_cluster



    #arithmetic mean of the mean distance between
    #the centroids and respective examples of all cluster of  the model
    #  density of normal cencept cluster
    def distance_mean_all_cluster(self):   #normal concept
        self.kmeans = KMeans(n_clusters=self.k, random_state=0).fit(self.X)        #k means algorithmus fitX
        distance_all = 0
        f_count=self.k
        for n in range(self.k):
            b = self.kmeans.transform(self.X)[np.where(self.kmeans.labels_ == n)]  # array
            if b.shape[0]<self.n_exin:
                f_count-=1
                continue
            else:
                '''mean distance between centroid and samples for each cluster(normal concept)'''
                c = np.mean(np.sqrt(np.sum((b ** 2), axis=1)))   #float
                distance_all += c
        distance_all_mean = distance_all / (f_count)
        return distance_all_mean


    '''max distance betwwen the centroid of the model(normal) and global centroid'''
    def d_max(self):
        centroid_k_offall=np.sum(self.kmeans.cluster_centers_,axis=0) /self.k   #List, gobal centroid
        centroids_k=self.kmeans.cluster_centers_           #array--all normal concept centroids
        d_max_List=[]
        for i in range(self.k):             #distance between each centroid and global centroid
            d=np.sqrt(np.sum(np.square(np.array(centroid_k_offall)-np.array(centroids_k[i]))))  #
            d_max_List.append(d)            #return to original list, not like np.append()
        d_max=max(d_max_List)
        return d_max,centroid_k_offall  # float, List


    '''
    k for candidatencluster
    '''
    def candidaten_cluster(self):
        if self.unknow.shape[0]>= self.short_term_memory:    #max number in unknow dataset out of range, find if any candidaten cluster

            #if k fit unknow dataset
            self.detect_k_cluster()

            #if k_cluster changed, self.k_unknow_cluster changes too
            self.k_unknow_cluster = KMeans(n_clusters=self.k_cluster, random_state=0).fit(self.unknow)

            ##candidate cluster not valid, go back to unknow
            k_cluster_new=np.empty((0,self.unknow.shape[1]))

            for i in range(self.k_cluster):

                e = self.k_unknow_cluster.transform(self.unknow)[np.where(self.k_unknow_cluster.labels_ == i)] #return to an array
                if e.shape[0]>=self.n_excl:
                    '''mean distance between the centroid and exampls of the candidate cluster'''
                    mean_distance_unknow = np.mean(np.sqrt(np.sum((e ** 2), axis=1)))
                    print("mean_distance_unknow",mean_distance_unknow,"distance_mean_all_cluster",self.distance_mean_all_cluster())
                    # if new_cluster enough density as normal concept cluster
                    if mean_distance_unknow > self.distance_mean_all_cluster():  #candidate cluster not valid, go back to unknow
                        for q in range(self.unknow.shape[0]):
                            if self.k_unknow_cluster.labels_[q]==i :
                                k_cluster_new=np.append(k_cluster_new,[self.unknow[q]],axis=0) #self.unknow[q] ->list
                    else:
                        ## candidate cluster valid
                        d, e = self.d_max()   # return d_max,centroid_k_offall   float, List
                        print("d_max",d)
                        d_max_=d
                        centroid_k_offall_=np.array(e)     # gobal centroid list->array

                        d_k_cluster=np.array(self.k_unknow_cluster.cluster_centers_[i])  #list->array

                        d_detect=np.sqrt(np.sum((d_k_cluster-centroid_k_offall_)**2))
                        print(d_detect)
                        if d_detect<=d_max_:

                            print("concept_drift detected",self.t_Y)
                        else:

                            print("novelty detected")
                else:
                    for n in range(self.unknow.shape[0]):
                        if self.k_unknow_cluster.labels_[n] == i:
                            k_cluster_new = np.append(k_cluster_new, [self.unknow[n]], axis=0)

            self.unknow=k_cluster_new
            '''
            after drift/novelty detected, those samples are no langer in slef.unknow, and it can continue to
            concept drift/novelty detection, based on normal concept and other unknow samples
            '''
        else:
            pass


