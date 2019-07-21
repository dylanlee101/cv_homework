# -*- coding: utf-8 -*-
# @Time     : 2019/7/21 17:03
# @Author   : Li Wenyi
# @File     : LogisticRegression.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class LogisticRegression():
    def __init__(self):
        #初始化
        self.coef = None
        self.intercept = None
        self._theta = None
    def sigmoid(self,t):
        return 1./(1.+ np.exp(-t))
    def fit(self,x_train,y_train,lr = 0.001,max_iter=10000):
        #使用梯度下降法进行训练
        def J(theta,x_list,gt_y_list):
            #目标函数
            pred_y = self.sigmoid(x_list.dot(theta))
            try:
                return -np.sum(gt_y_list * np.log(pred_y) + (1-gt_y_list) * np.log(1-pred_y)) / len(gt_y_list)
            except:
                return float('inf')
        def dJ(theta,x_list,gt_y_list):
            #求导
            return x_list.T.dot(self.sigmoid(x_list.dot(theta)) - gt_y_list) / len(gt_y_list)
        def gradient_descent(x_list,gt_y_list,initial_theta,lr,max_iter=10000,epsilon=1e-8):
            theta = initial_theta
            for i in range(max_iter):
                gradient = dJ(theta,x_list,gt_y_list)
                # print(gradient)
                last_theta = theta
                theta = theta - lr * gradient
                #early stop
                if abs(J(theta,x_list,gt_y_list) - J(last_theta,x_list,gt_y_list)) < epsilon:
                    break
            return theta
        x_list = np.hstack([np.ones((len(x_train),1)),x_train])
        inital_theta = np.zeros(x_list.shape[1])
        self._theta = gradient_descent(x_list,y_train,inital_theta,lr,max_iter)

        #截距,b
        self.intercept = self._theta[0]
        # x_i前的参数
        self.coef = self._theta[1:]
        print("theta :",self._theta)
        return self
    def predict(self,x_test,y_test):
        x_list = np.hstack([np.ones((len(x_test),1)),x_test])
        proba_y = self.sigmoid(x_list.dot(self._theta))
        pred_y = np.array(proba_y >0.5,dtype='int')
        print("pred_y:",pred_y)
        print("gt_y:",y_test)
        return pred_y


#使用鸢尾花数据进行测试
iris = datasets.load_iris()
x = iris.data
y = iris.target
#使用部分数据
x = x[y<2,:2]
y = y[y<2]

#显示数据
plt.scatter(x[y == 0,0],x[y == 0,1],color='red')
plt.scatter(x[y == 1,0],x[y == 1,1],color='blue')
plt.show()

#划分数据集
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1210)

#测试代码
log_reg = LogisticRegression()
log_reg.fit(x_train,y_train)
pred_y = log_reg.predict(x_test,y_test)
#使用sklearn的评价函数
print("acc:",accuracy_score(y_test,pred_y))

