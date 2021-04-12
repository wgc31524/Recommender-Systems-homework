import numpy as np
import random
from data import *

class pmf():
    def __init__(self, 
                 train_list,           
                 test_list,             
                 N,                     
                 M,                     
                 K=10,                  
                 learning_rate=0.001,  
                 lamda_regularizer=0.1, 
                 max_iteration=50      
                ):
        self.train_list = train_list
        self.test_list = test_list
        self.N = N
        self.M = M
        self.K = K
        self.learning_rate = learning_rate
        self.lamda_regularizer = lamda_regularizer
        self.max_iteration = max_iteration
    
    
    def train(self):
        P = np.random.normal(0, 0.1, (self.N, self.K))
        Q = np.random.normal(0, 0.1, (self.M, self.K))

        train_mat = sequence2mat(sequence = self.train_list, N = self.N, M = self.M)
        test_mat = sequence2mat(sequence = self.test_list, N = self.N, M = self.M)

        records_list = []
        for step in range(self.max_iteration):
            los=0.0
            for data in self.train_list:
                u,i,r = data
                P[u],Q[i],ls = self.update(P[u], Q[i], r=r, 
                                           learning_rate=self.learning_rate, 
                                           lamda_regularizer=self.lamda_regularizer)
                los += ls
            pred_mat = self.prediction(P,Q)
            mae,rmse = mae_rmse(pred_mat, test_mat)
            records_list.append(np.array([los, mae, rmse]))

            if step % 10 ==0:
                print(' step:%d \n loss:%.4f,mae:%.4f,rmse:%.4f'
                      %(step,los,mae,rmse))

        print(' end. \n loss:%.4f,mae:%.4f,rmse:%.4f,'
              %(records_list[-1][0],records_list[-1][1],records_list[-1][2]))
        return P, Q, np.array(records_list)


    def update(self, p, q, r, learning_rate=0.001, lamda_regularizer=0.1):
        e = r - np.dot(p, q.T)            
        p = p + learning_rate*(e*q - lamda_regularizer*p) #梯度下降
        q = q + learning_rate*(e*p - lamda_regularizer*q)
        loss = 0.5 * (error**2 + lamda_regularizer*(np.square(p).sum() + np.square(q).sum())) #损失函数
        return p, q, loss


    def prediction(self, P, Q):
        N,K = P.shape
        M,K = Q.shape

        rating_list=[]
        for u in range(N):
            u_rating = np.sum(P[u,:]*Q, axis=1)
            rating_list.append(u_rating)
        r_pred = np.array(rating_list)
        return r_pred
        
    def mae_rmse(r_pred, test_mat):
        y_pred = r_pred[test_mat>0]
        y_true = test_mat[test_mat>0]
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return mae, rmse
        def sequence2mat(sequence, N, M):
            records_array = np.array(sequence)
            mat = np.zeros([N,M])
            row = records_array[:,0].astype(int)
            col = records_array[:,1].astype(int)
            values = records_array[:,2].astype(np.float32)
            mat[row,col]=values
        
        return mat
    def recall_precision(topn, test_mat):
        n,m = test_mat.shape
        hits,total_pred,total_true = 0.,0.,0.
        for u in range(n):
            hits += len([i for i in topn[u,:] if test_mat[u,i]>0])
            size_pred = len(topn[u,:])
            size_true = np.sum(test_mat[u,:]>0,axis=0)
            total_pred += size_pred
            total_true += size_true

        recall = hits/total_true
        precision = hits/total_pred
        return recall, precision
    def sequence2mat(sequence, N, M):
        # input:
        # sequence: the list of rating information
        # N: row number, i.e. the number of users
        # M: column number, i.e. the number of items
        # output:
        # mat: user-item rating matrix
        records_array = np.array(sequence)
        mat = np.zeros([N,M])
        row = records_array[:,0].astype(int)
        col = records_array[:,1].astype(int)
        values = records_array[:,2].astype(np.float32)
        mat[row,col]=values
        
        return mat
