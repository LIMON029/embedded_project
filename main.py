# -*- coding: utf-8 -*-
import random

from Utils import *

font = cv2.FONT_HERSHEY_SIMPLEX
direction = 0

#N_SLICES만큼 이미지를 조각내서 Images[] 배열에 담는다
Images = []
N_SLICES = 6

for q in range(N_SLICES):
    Images.append(Image())

imgs = []

for i in range(4):
    imgs.append(cv2.imread('./test_data/left%d.jpg' % i))
    imgs.append(cv2.imread('./test_data/right%d.jpg' % i))
imgs.append(cv2.imread('./test_data/dave_1.jpg'))
imgs.append(cv2.imread('./test_data/dave.jpg'))
imgs.append(cv2.imread('./test_data/straight0.jpg'))
imgs.append(cv2.imread('./test_data/straight1.jpg'))
imgs.append(cv2.imread('./test_data/none.jpg'))
random.shuffle(imgs)

for img in imgs:
    if img is not None:
        cols, rows, _ = img.shape

        #이미지를 조각내서 윤곽선을 표시하게 무게중심 점을 얻는다
        Points, weight = SlicePart(img, Images, N_SLICES)
        print('Points : ', Points)

        #N_SLICES 개의 무게중심 점을 x좌표, y좌표끼리 나눈다
        x = []
        y = []
        for i in range(N_SLICES):
            x.append(Points[i][0])
            y.append(Points[i][1])

        #조각난 이미지를 한 개로 합친다
        fm = RepackImages(Images)
        print(weight)
        direction = SendCommand(weight)
        #완성된 이미지를 표시한다
        cv2.imshow("Vision Race", fm)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    else:
        print('not even processed')

print('finish')