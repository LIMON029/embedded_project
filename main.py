# -*- coding: utf-8 -*-
import random
import serial
import time
from Utils import *
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0

# ser = serial.Serial('/dev/ttyUSB0', 9600)
# if ser is None:
#     ser = serial.Serial('/dev/ttyUSB0', 9600)

#N_SLICES만큼 이미지를 조각내서 Images[] 배열에 담는다
Images = []
Last_Images = []
Temp_Images = []
N_SLICES = 6

for q in range(N_SLICES):
    Images.append(Image())
    Last_Images.append(Image())
    Temp_Images.append(Image())

imgs = []

# for i in range(4):
#     imgs.append(cv2.imread('./test_data/left%d.jpg' % i))
#     imgs.append(cv2.imread('./test_data/right%d.jpg' % i))
# imgs.append(cv2.imread('./test_data/dave_1.jpg'))
imgs.append(cv2.imread('./test_data/dave.jpg'))
# imgs.append(cv2.imread('./test_data/straight0.jpg'))
# imgs.append(cv2.imread('./test_data/straight1.jpg'))
# imgs.append(cv2.imread('./test_data/none.jpg'))
imgs.append(cv2.imread('./test_data/qr.jpg'))

for img in imgs:
    if img is not None:
        cols, rows, _ = img.shape
        stop = False

        #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
        Points, weight, last, last_w = SlicePart(img, Images, N_SLICES)
        last_img = last.copy()
        _, _, last, _ = SlicePart(last_img, Temp_Images, 3)
        _, last_weight = LastSlicePart(last, Last_Images, N_SLICES)
        print('Points : ', Points)

        #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
        x = []
        y = []
        for i in range(N_SLICES):
            x.append(Points[i][0])
            y.append(Points[i][1])

        det = cv2.QRCodeDetector()
        retval, points, straight_qrcode = det.detectAndDecode(img)
        if points.size == 0:
            stop = True

        if not stop:
            #조각난 이미지를 한 개로 합친다
            fm = RepackImages(Images)
            last_fm = RepackImages(Last_Images)
            print(weight)
            print(last_weight)

            # direction = SendCommand(ser, weight, last_weight, last_w)
            direction = SendCommand('', weight, last_weight, last_w)
            #완성된 이미지를 표시한다
            cv2.imshow("Vision Race_%c"%(direction), fm)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
    else:
        print('not even processed')

print('finish')