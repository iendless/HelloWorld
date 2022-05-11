import cv2
import os

# 输入图片地址和对应图片道路边缘点集的地址, 返回凸包点集
def getHull(imgPath, pointsPath):
    pass;

# 输入凸包点集, 和检测框下边缘线段的两端点坐标, 返回分数
def getScoreFromHull(hull, pointA, pointB):
    pass;

testDataSet = "./my_test/test.txt"

testDataFile = open(testDataSet, r)
