# -*- coding: utf-8 -*-
# @Time     : 2019/7/13 15:13
# @Author   : Li Wenyi
# @File     : ransac.py
import random
def ransacMatching(A, B,n_iter):
    #相似性阈值
    threshold = 3
    #循环次数
    k = 2000
    #不再变化次数
    nochange = n_iter
    #随机选取初始四个点
    inliers = random.sample([A,B],4)
    outlier = A.remove(inliers)
    while(k > 0 and nochange >0):
        #计算homography
        model = findHomography(inliers)
        #测试外点
        for i in outlier:
            value = model.cal(i)
            if value < threshold:
                inliers.append(i)
                outlier.remove(i)
                nochange = n_iter
            else:
                nochange -= 1
        k -= 1
def findHomography(inliers):
    print("findHomography")