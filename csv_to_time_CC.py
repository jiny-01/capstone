import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 파일 경로
path = 'C:/Users/82103/Desktop/mean/'

ndvi_file = path + 'NDVI_EVI_mean/ndvi/Hungary_ndvi_timeseries.csv'
LST_file = path + 'LST_mean/Hungary_LST_timeseries.csv'
drought_file = path + 'Drought_mean/Hungary_drought_timeseries.csv'

# CSV 파일 읽기 (인코딩 설정 추가)
ndvi_data = pd.read_csv(ndvi_file, encoding='utf-8')
LST_data = pd.read_csv(LST_file, encoding='utf-8')
drought_data = pd.read_csv(drought_file, encoding='utf-8')

# NaN 값 0으로 채우기
ndvi_data['mean'].fillna(0, inplace=True)
LST_data['mean'].fillna(0, inplace=True)
drought_data['mean'].fillna(0, inplace=True)

# 각 지수를 정규화
ndvi_normalized = (ndvi_data['mean'] - ndvi_data['mean'].min()) / (ndvi_data['mean'].max() - ndvi_data['mean'].min())
LST_normalized = (LST_data['mean'] - LST_data['mean'].min()) / (LST_data['mean'].max() - LST_data['mean'].min())
drought_normalized = (drought_data['mean'] - drought_data['mean'].min()) / (drought_data['mean'].max() - drought_data['mean'].min())

# 그래프 설정
plt.figure(figsize=(20, 6))

# NDVI 그래프
ndvi_x = range(0, len(ndvi_normalized))
plt.plot(ndvi_x, ndvi_normalized, label='NDVI')

# LST 그래프
LST_x = range(len(LST_normalized))
plt.plot(LST_normalized, label='LST')

# Drought 그래프
drought_x = range(len(drought_normalized))
plt.plot(drought_normalized, label='Drought')

# x축 레이블 설정
xtick = [i for i in range(0, len(LST_data['mean']))]
dates = [str(date) for date in LST_data['date']]
plt.xticks(xtick, dates, rotation=45)

# 축 레이블 및 제목 설정
plt.xlabel('Year', fontsize=15)
plt.ylabel('Normalized Value', fontsize=15)
plt.title('Time Series Comparison (Hungary)', fontsize=20, pad=15)
plt.grid(True, linestyle='--')

# 상관계수 구하기
ndvi_lst_corr = np.corrcoef(ndvi_data['mean'], LST_data['mean'])[0, 1]
ndvi_drought_corr = np.corrcoef(ndvi_data['mean'], drought_data['mean'])[0, 1]
lst_drought_corr = np.corrcoef(LST_data['mean'], drought_data['mean'])[0, 1]

# 상관계수 텍스트 생성
corr_text = 'Correlation Coefficients:\n'
corr_text += 'NDVI-Drought: {:.2f}, '.format(ndvi_drought_corr)
corr_text += 'LST-Drought: {:.2f}, '.format(lst_drought_corr)
corr_text += 'NDVI-LST: {:.2f}'.format(ndvi_lst_corr)

# 그래프 표시
plt.legend()
plt.text(0.02, -0.2, corr_text, transform=plt.gca().transAxes, fontsize=12)
plt.show()
