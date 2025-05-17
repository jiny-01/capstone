import os
import fnmatch as fm
import numpy as np
import cartopy.crs as crs
import matplotlib.cm as mcm
import matplotlib.pyplot as plt
import warnings as wa

#--폴더 설정 및 파일 목록 불러오기
wa.filterwarnings(action='ignore')
out_dir = 'c:/temp/npp_png'  #결과 저장할 폴더
in_dir = 'c:/temp/npp_dat'
files = os.listdir(in_dir)
dat = fm.filter(files, '*.dat')

#--위경도 설정
#위도(lat), 경도(lon) 좌표를 셀 단위로 만듦 (총 2400 x 1680 크기의 그리드)
cell = 1/240
half = cell/2
lons = np.arange(124+half, 131-half, cell)
lats = np.arange(33+half, 43-half, cell)
prj = crs.PlateCarree()       #PlateCarree 투영법 사용(일반 지도)
lgnd = mcm.get_cmap('Greens', 64)

for a_file in dat:
    print(a_file)
    a_path = os.path.join(in_dir,a_file)
    #데이터 불러오기 및 전처리
    npp = np.fromfile(a_path, dtype='int16')
    npp = npp.astype('float32')
    npp[npp > 32700] = np.nan
    npp[npp < -30000] = np.nan
    npp = npp*0.0001
    #통계 출력
    print('최소=', np.nanmin(npp))
    print('최대=', np.nanmax(npp))
    print('평균=', np.nanmean(npp))
    print()
    #배열 변환 및 시각화 - 데이터를 2차원 그리드로 변형
    npp = npp.reshape(2400,1680)
    npp = np.flipud(npp)
    png = os.path.join(out_dir,a_file+'.png')
    ax = plt.axes(projection=prj)
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    plt.pcolormesh(lons, lats, npp, transform=prj, cmap=lgnd, vmin=0, vmax=1.3)
    plt.title('NPP'+a_file[12:16], pad=10)
    plt.colorbar(extend='max', pad=0.15, label='(kg C/m2)')
    #이미지 저장
    plt.savefig(png, dpi=200)
    plt.close()
