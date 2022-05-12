import cv2
import os
import numpy as np

# 输入图片地址和对应图片道路边缘点集的地址, 返回凸包点集
# img -> mat
# points -> list[cv2::point2D]
def getHull(img, points):
    hull = cv2.convexHull(points)

    # 测试凸包正确性
    # cv2.polylines(img, [hull], True, (255,255,0), 2)
    # cv2.imwrite("./testHull.jpg", img)

    return hull

# 输入凸包点集, 检测框左上和右下的两对角线端点坐标, 返回分数
    # 存在改进的空间- 理论上应该按照物体占了道路的部分在道路整体的百分比而不是物体本身的百分比进行评分
def getScoreFromHull(hull, pointA, pointB) -> float:
    pointL = []
    pointR = []
    pointL.append(pointA[0])
    pointL.append(pointB[1])
    pointR = pointB[:]
    len = int(pointR[0] - pointL[0] + 1)
    # print(pointL)
    # print(pointR)
    # print(len)
    # print("\n")
    i = pointL[0]
    score = 0
    itemNum = 0
    while(i <= pointR[0]):
        itemNum += 1
        curS = cv2.pointPolygonTest(hull, (pointL[0]+i, pointL[1]), False)
        if curS == 1:
            score += 1
        i += len/10
    
    return score/itemNum

testSet = "./my_test/test.txt"
testSetFile = open(testSet, "r")
testDir = "./my_test/byCulane/image_mapillary_pred/"

bboxFilePath = testDir+"KTTI_demo/stixelBBox.txt"
bboxFile = open(bboxFilePath, "r")
# 初始化map, 存储<string, vector<point>>, string 为图片名, vector 为对应图片bbox 点集
bboxMap = {}
for line in bboxFile.readlines():
    if line[0] != '(' :
        index = line.strip('\n')
        bboxMap[index] = []
        continue
    pointStr = line.strip('\n').lstrip('(').rstrip(')').split(',')
    x = int(pointStr[0])
    y = int(pointStr[1])
    point = []
    point.append(x)
    point.append(y)
    bboxMap[index].append(point)
        
    

# 这些代码应该是系统不需要的, 这是我在本地的测试代码

# 对于每个测试图片先提取道路边缘点集, 再根据图片名, 在bboxMap 中取出障碍物位置进行评分
for line in testSetFile.readlines():
    testImgPath = testDir + line.strip("\n")
    testImgName = line.strip("\n").split('/')[-1]
    testPointsPath = testDir + line.strip("\n")[:-4] + ".txt"
    testImg = cv2.imread(testImgPath)
    testPointsStr = open(testPointsPath, "r").readlines()
    testPoints = []
    for pointStr in testPointsStr:
        point = []
        pointStr = pointStr.strip('\n').lstrip('(').rstrip(')').split(',')
        x = int(pointStr[0])
        y = int(pointStr[1])
        point.append(x)
        point.append(y)
        testPoints.append(point)
    hull = getHull(testImg, np.array(testPoints))
    # print(hull)

    print(testImgName)
    bboxList = bboxMap[testImgName]
    # print(bboxList)
    for i in range(0, len(bboxList), 2):
        pointA = bboxList[i]
        pointB = bboxList[i+1]
        score = getScoreFromHull(hull, pointA, pointB)
        print(score)






