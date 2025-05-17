import numpy as np
import PIL.Image as img
import matplotlib.colors as col
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as ft

#1. 지도 투영법 설정 (EPSG:4326, 일반 GPS 좌표계)
epsg_4326 = ccrs.PlateCarree() #GPS 좌표계
ax = plt.axes(projection=epsg_4326) #XY축 공간 생성
# 2. 축 눈금 설정 (위경도 라벨)
ax.set_xticks(np.linspace(126, 130, 5), crs=epsg_4326)
ax.set_yticks(np.linspace(34, 38, 5), crs=epsg_4326)
# 3. 배경 지형 요소 추가
ax.add_feature(ft.LAND)
ax.add_feature(ft.RIVERS)
ax.add_feature(ft.OCEAN)
ax.add_feature(ft.COASTLINE)
ax.add_feature(ft.BORDERS, linestyle=':')
# 4. 산림 분포 이미지 불러오기
map = img.open('c:/temp/sk_forest.tif') #경로변경시 오답처리
nda = np.array(map, dtype='float32')
nda[nda == -9999] = np.nan
# 5. 이미지 범위 지정 (경도 126~130, 위도 34~38)
ext = [126, 130, 34, 38]
# 6. 산림 유형 색상 설정 (범례용 컬러맵)
colors = ['red', 'orange', 'yellow', 'green', 'blue']
pal = col.ListedColormap(colors)
# 7. 이미지 지도 위에 그리기
draw = ax.imshow(nda, extent=ext, cmap=pal, interpolation='none') #이미지 생성
# 8. 컬러바 추가 및 라벨 지정
plt.rc('font', family='Malgun Gothic')
cbar = plt.colorbar(draw, ticks=[1,2,3,4,5]) #컬러바 넣기
cbar.ax.set_yticklabels(['상록침엽수림','상록활엽수림','낙엽침엽수림','낙엽활엽수림','혼효림'])
plt.title('Forest Map') #타이틀 넣기
plt.savefig('c:/temp/forest.png')
