import os
import numpy as np
import PIL.Image as img
import matplotlib.cm as mcm
import matplotlib.pyplot as plt

#데이터 불러오기
in_dir = 'c:/temp/tif_small'
R_img = img.open(os.path.join(in_dir, 'band4.tif'))
G_img = img.open(os.path.join(in_dir, 'band3.tif'))
B_img = img.open(os.path.join(in_dir, 'band2.tif'))

#배열 변환 & 결측값 처리 - TIFF 이미지를 NumPy 배열로 변환
R_nda = np.asarray(R_img, dtype='float32')
G_nda = np.asarray(G_img, dtype='float32')
B_nda = np.asarray(B_img, dtype='float32')
#결측값 처리
R_nda[R_nda == -9999] = np.nan
G_nda[G_nda == -9999] = np.nan
B_nda[B_nda == -9999] = np.nan

#5~95퍼센타일 기준으로 스트레칭한 트루컬러 이미지 생성
R_min, R_max = np.nanpercentile(R_nda, [5, 95])
G_min, G_max = np.nanpercentile(G_nda, [5, 95])
B_min, B_max = np.nanpercentile(B_nda, [5, 95])

#RGB 정규화 및 트루컬러 이미지 생성
R_val = (R_nda - R_min) / (R_max - R_min)
R_val[R_val < 0] = 0
R_val[R_val > 1] = 1
R_val = np.round(R_val * 255)

G_val = (G_nda - G_min) / (G_max - G_min)
G_val[G_val < 0] = 0
G_val[G_val > 1] = 1
G_val = np.round(G_val * 255)

B_val = (B_nda - B_min) / (B_max - B_min)
B_val[B_val < 0] = 0
B_val[B_val > 1] = 1
B_val = np.round(B_val * 255)

rgb = np.dstack((R_val, G_val, B_val))
rgb = rgb.astype('uint8')
rgb_img = img.fromarray(rgb)
rgb_img.save('c:/temp/true_color.jpg')

#RGI(Red-Green Index) 계산 및 시각화
#RGI(Red Green Index): 고사한 식생이 큰값을 가짐
rgi = R_nda / (G_nda + 0.01)  # 분모에 0.01을 더해 0으로 나누는 오류 방지
cmin = 0
cmax = 1
lgnd = mcm.get_cmap('rainbow', 10)
#RGI 시각화 및 저장
plt.imshow(rgi, cmap=lgnd, vmin=cmin, vmax=cmax)
plt.colorbar()
plt.savefig('c:/temp/rgi.png')
