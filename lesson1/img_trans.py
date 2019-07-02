# -*- coding: utf-8 -*-
# @Time     : 2019/7/2 20:27
# @Author   : Li Wenyi
# @File     : img_trans.py
import cv2
import random
import numpy as np

img_path = "lena.jpg"
class Augmentation():
    def __init__(self,img_path):
        self.img = cv2.imread(img_path)
    def img_crop(self,x1,y1,x2,y2):
        #参数：需要剪切的左上角和右下角的四个坐标值
        return self.img[y1:y2,x1:x2]
    def random_light_color(self,min_val,max_val):
        #参数：颜色改变的的范围
        B,G,R = cv2.split(self.img)
        for B_ in [B,G,R]:
            b_rand = random.randint(min_val,max_val)
            if b_rand == 0:
                pass
            elif b_rand > 0:
                lim = 255 - b_rand
                B_[B_>lim] = 255
                B_[B_<=lim] = (b_rand+B_[B_<=lim]).astype(self.img.dtype)
            elif b_rand < 0:
                lim = 0-b_rand
                B_[B_<lim] = 0
                B_[B_>=lim] = (b_rand + B_[B_>=lim]).astype(self.img.dtype)
        img_merge = cv2.merge((B,G,R))
        return img_merge
    def adjust_gamma(self,gamma=1.0):
        # 参数：gamma值
        invGamma = 1.0 / gamma
        table = []
        for i in range(256):
            table.append(((i/255.0) ** invGamma)*255)
        table = np.array(table).astype("uint8")
        return cv2.LUT(self.img,table)
    def rotate(self,center,angle = 30,scale = 1.):
        #参数：旋转中心坐标（x，y），旋转角度，缩放比例
        col,row = self.img.shape[:2]
        M = cv2.getRotationMatrix2D(center, angle, scale)
        img_rotate = cv2.warpAffine(self.img, M, (col, row))
        return img_rotate
    def img_flip(self,flip=1):
        #参数：翻转参数，0：垂直翻转 1：水平翻转 -1：垂直水平翻转
        return cv2.flip(self.img,flip)

    def random_wrap(self, col, row,random_margin = 60):
        #参数 投影变换后的 height，width，以及变换的margin
        height, width, channels = self.img.shape
        # wrap:
        x1 = random.randint(-random_margin, random_margin)
        y1 = random.randint(-random_margin, random_margin)
        x2 = random.randint(width - random_margin - 1, width - 1)
        y2 = random.randint(-random_margin, random_margin)
        x3 = random.randint(width - random_margin - 1, width - 1)
        y3 = random.randint(height - random_margin - 1, height - 1)
        x4 = random.randint(-random_margin, random_margin)
        y4 = random.randint(height - random_margin - 1, height - 1)

        dx1 = random.randint(-random_margin, random_margin)
        dy1 = random.randint(-random_margin, random_margin)
        dx2 = random.randint(width - random_margin - 1, width - 1)
        dy2 = random.randint(-random_margin, random_margin)
        dx3 = random.randint(width - random_margin - 1, width - 1)
        dy3 = random.randint(height - random_margin - 1, height - 1)
        dx4 = random.randint(-random_margin, random_margin)
        dy4 = random.randint(height - random_margin - 1, height - 1)

        pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        pts2 = np.float32([[dx1, dy1], [dx2, dy2], [dx3, dy3], [dx4, dy4]])
        M_warp = cv2.getPerspectiveTransform(pts1, pts2)
        img_warp = cv2.warpPerspective(self.img, M_warp, (col, row))
        return M_warp, img_warp

aug = Augmentation(img_path)
img_crop = aug.img_crop(20,30,200,200)
change_color = aug.random_light_color(-60,60)
gamma = aug.adjust_gamma(2)
rotate = aug.rotate((200,200),40,0.8)
h_flip = aug.img_flip()
v_flip = aug.img_flip(0)
hv_flip = aug.img_flip(-1)
m_rarp,wrap = aug.random_wrap(500,500,65)

cv2.imshow("img_crop",img_crop)
cv2.imshow("change color",change_color)
cv2.imshow("gamma",gamma)
cv2.imshow("rotate",rotate)
cv2.imshow("h_flip",h_flip)
cv2.imshow("v_flip",v_flip)
cv2.imshow("hv_flip",hv_flip)
cv2.imshow("wrap",wrap)
cv2.waitKey()
cv2.destroyAllWindows()
