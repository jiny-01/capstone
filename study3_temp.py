# -*- coding: utf-8 -*-

#%%라이브러리 설치
#conda install -c conda-forge pyhdf
#pip install matplotlib
#pip install basemap
#pip install basemap-data-hires

#%% 라이브러리 
from pyhdf.SD import SD, SDC
import numpy as np
import matplotlib.pyplot as plt
import glob, os, sys
os.environ["PROJ_LIB"] = "C:/Users/82103/miniconda3/Library/share/"
from mpl_toolkits.basemap import Basemap
import pandas as pd
import datetime

#%% 자료 내 위치 찾기
def great_circle(lon1, lat1, lon2, lat2):
    #lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    ## lon1 & lat1 : 위성 자료의 경도 & 위도
    ## lon2 & lat2 : 지점 자료의 경도 & 위도
    
    pi = np.double(np.pi)    
    deg2rad = pi / np.double(180.)
    
    sinlat1 = np.sin(lat1 * deg2rad)
    sinlat2 = np.sin(lat2 * deg2rad)
    coslat1 = np.cos(lat1 * deg2rad)
    coslat2 = np.cos(lat2 * deg2rad)
    dlon = np.abs(lon1-lon2)
    cosdlon = np.cos(dlon * deg2rad)
        
    return 6371 * (np.arccos(sinlat1 * sinlat2 + coslat1 * coslat2 * cosdlon))
#%% 위경도 생산 및 필요한 지점 설정

# gridsize = 0.05
# lat = (np.arange(1,3601,1) * gridsize) - (gridsize/2) - 90
# lat = np.flip(lat)
# lon = (np.arange(0,7200,1) * gridsize) + (gridsize/2) - 180
# lat = np.round(lat, 3)
# lon = np.round(lon, 3)

# lat_2d = np.zeros((3600,7200))
# lon_2d = np.zeros((3600,7200))
# for i in range(0,7200): lat_2d[:,i] = lat[:]
# for i in range(0,3600): lon_2d[i,:] = lon[:]

gpath = 'C:/Users/82103/Desktop/geo/'
nx = 1340; ny = 900

lat_2d = np.fromfile(gpath+'MODIS_lat.bin', dtype=np.float32).reshape(ny,nx)
lon_2d = np.fromfile(gpath+'MODIS_lon.bin', dtype=np.float32).reshape(ny,nx)

lat = lat_2d[:,0]
lon = lon_2d[0,:]


lower_left = [46, 20]
upper_right = [49, 23]


lower_left = great_circle(lon_2d, lat_2d, lower_left[1], lower_left[0])               
lower_left_minloc = np.where(lower_left == np.min(lower_left))
lat_lower_ind = lower_left_minloc[0][0]
lon_lower_ind = lower_left_minloc[1][0]

upper_right = great_circle(lon_2d, lat_2d, upper_right[1], upper_right[0])             
upper_right_minloc = np.where(upper_right == np.min(upper_right))
lat_upper_ind = upper_right_minloc[0][0]
lon_upper_ind = upper_right_minloc[1][0]

#%% 파일 경로 및 자료 읽기
path = 'C:/Users/82103/Desktop/mean/LST_mean/'
fn = glob.glob(path + '*.bin')
fn.sort()

df = pd.DataFrame()
sum_date = []
sum_europe = []

mask = np.fromfile(path+'modis_land_sea_mask.bin', dtype=np.int8).reshape(ny,nx)


for file in fn : 
    ndvi = np.fromfile(file, dtype=np.float32).reshape(ny,nx)
    
    #%%자료 자르기 및 평균 계산
    cut_ndvi = ndvi[lat_upper_ind : lat_lower_ind, lon_lower_ind : lon_upper_ind]
    cut_lat = lat[lat_upper_ind : lat_lower_ind]
    cut_lon = lon[lon_lower_ind : lon_upper_ind]
    
    cut_mask = mask[lat_upper_ind : lat_lower_ind, lon_lower_ind : lon_upper_ind]
    
    cut_ndvi = np.where(cut_mask == 0, np.nan, cut_ndvi)

    mean_ndvi = np.nanmean(cut_ndvi)    

    #%% 데이터 출력
    file_name = os.path.basename(file)
    date = file_name[:4]  # 연도 정보만 추출
    cal_date = str(datetime.datetime.strptime(date, '%Y').date().year)

    sum_date.append(cal_date)
    sum_europe.append(mean_ndvi)    
    
df['date'] = sum_date
df['mean'] = sum_europe

#%%
df['mean'].fillna(0, inplace=True)

# 그래프 설정
plt.figure(figsize=(25, 6))
plt.plot(df['mean'], marker='o')

xtick = [i for i in range(0,len(df['mean'])+1,2)]
dates = [df['date'][i] for i in xtick]

plt.xticks(xtick,dates)

# 축 레이블 및 제목 설정
plt.xlabel('Date', fontsize=15)
plt.ylabel('ndvi_mean',fontsize=15)
plt.title('Hungary LST timeseries',fontsize=20, pad=15)
plt.grid(True, linestyle='--')

plt.ylim(0,1)

# x축 레이블 회전
plt.xticks(rotation=45)

# 그래프 표시
plt.show()

df.to_csv(path + 'Hungary11_LST_timeseries.csv')
