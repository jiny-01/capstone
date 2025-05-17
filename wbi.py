import cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as img

#이미지 불러오기 및 배열 변환
im = img.open('c:/temp/wbi.tif')
nda = np.array(im)  # Numpy 배열로 변환

#정규화 (0~255 로 스케일링)
#이미지 데이터를 0~255 범위로 정규화
#wbi는 이진화 및 블러 처리를 위한 데이터
w_min = np.nanmin(im)
w_max = np.nanmax(im)
wbi = (nda-w_min)/(w_max-w_min)*255

#이진화
retval, result = cv2.threshold(wbi, 155, 255, cv2.THRESH_BINARY)
#픽셀값이 **155 이상이면 255(흰색), 아니면 0(검정)**으로 바꿈
plt.imshow(result)
plt.title('Threshold 155/255')
plt.savefig('c:/temp/155.png')

#가우시안 블러 & 이진화
gauss = cv2.GaussianBlur(wbi, (5,5), cv2.BORDER_DEFAULT)
retval, result = cv2.threshold(gauss, 150, 255, cv2.THRESH_BINARY)
plt.imshow(result)
plt.title('Threshold 150/255 with 5x5 GF')
plt.savefig('c:/temp/150GF.png')

"""
위성 영상, 식생지수(NDVI), WBI 등에서 특정 값 이상만 추출할 때 사용
객체 검출 전처리, 식생지역 분리, 이미지 마스크 생성 등에 활용 가능
"""