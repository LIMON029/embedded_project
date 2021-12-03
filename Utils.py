# -*- coding: utf-8 -*-
import serial
import numpy as np
from Image import *

# 그림을 slices 의 수만큼 조각낸다
def SlicePart(im, images, slices):
    height, width = im.shape[:2]
    sl = int(height / slices);
    points = []
    minus_weights_cnt = 0
    plus_weights_cnt = 0
    minus_weights = []
    plus_weights = []
    last_weight = 0

    for i in range(slices):
        part = sl * i
        crop_img = im[part:part + sl, 0:width]
        # 조각난 이미지 crop_img를 images[]에 저장
        images[i].image = crop_img
        # Image.py에서 윤곽선을 그리고 무게중심을 표시
        cPoint, weight = images[i].Process()
        points.append(cPoint)
        if weight < 0:
            minus_weights_cnt += 1
            if last_weight > 0:
                minus_weights.clear()
                minus_weights_cnt = 0
            minus_weights.append(weight)
        elif weight > 0:
            plus_weights_cnt += 1
            if last_weight < 0:
                plus_weights.clear()
                plus_weights_cnt = 0
            plus_weights.append(weight)
        last_weight = weight
    if plus_weights_cnt > minus_weights_cnt:
        return points, plus_weights
    else:
        return points, minus_weights


# 조각난 이미지를 다시 합친다
def RepackImages(images):
    img = images[0].image
    for i in range(len(images)):
        if i == 0:
            img = np.concatenate((img, images[1].image), axis=0)
        if i > 1:
            img = np.concatenate((img, images[i].image), axis=0)
    return img


def Center(moments):
    if moments["m00"] == 0:
        return 0

    x = int(moments["m10"] / moments["m00"])
    y = int(moments["m01"] / moments["m00"])

    return x, y


def RemoveBackground(image, b):
    up = 100
    # create NumPy arrays from the boundaries
    lower = np.array([0, 0, 0], dtype="uint8")
    upper = np.array([up, up, up], dtype="uint8")
    # ----------------COLOR SELECTION-------------- (Remove any area that is whiter than 'upper')
    if b == True:
        mask = cv2.inRange(image, lower, upper)
        image = cv2.bitwise_and(image, image, mask=mask)
        image = cv2.bitwise_not(image, image, mask=mask)
        image = (255 - image)
        return image
    else:
        return image
    # ////////////////COLOR SELECTION/////////////


def SendCommand(weight):
    # ser = serial.Serial('/dev/ttyUSB0', 9600)
    # if ser is None:
    #     ser = serial.Serial('/dev/ttyUSB0', 9600)

    if weight.count(max(weight, key=weight.count)) > len(weight)/2:
        direction = 'G'
        if max(weight, key=weight.count) == 1:
            direction = 'B'
    else:
        if weight[0] < 0:
            direction = weight[1] - weight[0] < 0 and 'L' or 'R'
        if weight[0] > 0:
            direction = weight[1] - weight[0] > 0 and 'R' or 'L'

    print(direction)
    return direction
