# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

# 경로 설정
path = 'D:/capstone/csv/'

# CSV 파일 읽기
ndvi = pd.read_csv(path + '2016_2021_hungary_ndvi.csv', encoding='euc-kr')
drou = pd.read_csv(path + '2016_2021_hungary_temp.csv', encoding='euc-kr')
temp = pd.read_csv(path + '2016_2021_hungary_drought.csv', encoding='euc-kr')
prec = pd.read_csv(path + '2016_2021_hungary_precipitation.csv', encoding='euc-kr')


ndvi['파일명'] = pd.to_datetime(ndvi['파일명'], format='%Y%m%d')
drou['파일명'] = pd.to_datetime(drou['파일명'], format='%Y%m%d')
temp['파일명'] = pd.to_datetime(temp['파일명'], format='%Y%m%d')
prec['파일명'] = pd.to_datetime(prec['파일명'], format='%Y%m%d')

ndvi['date'] =  ndvi['파일명'].dt.strftime('%Y%m')
drou['date'] =  drou['파일명'].dt.strftime('%Y%m')
temp['date'] =  temp['파일명'].dt.strftime('%Y%m')
prec['date'] =  prec['파일명'].dt.strftime('%Y%m')

mean_ndvi = ndvi.groupby(['date']).mean().reset_index()
mean_drou = drou.groupby(['date']).mean().reset_index()
mean_temp = temp.groupby(['date']).mean().reset_index()
mean_prec = prec.groupby(['date']).mean().reset_index()

ndvi = np.array(mean_ndvi['평균값'])
drou = np.array(mean_drou['평균값'])
temp = np.array(mean_temp['평균값'])
prec = np.array(mean_prec['평균값'])

ndvi_normalized = (mean_ndvi['평균값'] - mean_ndvi['평균값'].min()) / (mean_ndvi['평균값'].max() - mean_ndvi['평균값'].min())
maxtemp_normalized = (mean_temp['평균값'] - mean_temp['평균값'].min()) / (mean_temp['평균값'].max() - mean_temp['평균값'].min())
drought_normalized = (mean_drou['평균값'] - mean_drou['평균값'].min()) / (mean_drou['평균값'].max() - mean_drou['평균값'].min())
precipitation_normalized = (mean_prec['평균값'] - mean_prec['평균값'].min()) / (mean_prec['평균값'].max() - mean_prec['평균값'].min())


plt.figure(figsize=(30, 6))
plt.plot(ndvi_normalized, label='NDVI')
plt.plot(maxtemp_normalized, label='Drought code')
plt.plot(drought_normalized, label='Max Temperature')
plt.plot(precipitation_normalized, label='Precipitation')


xtick = [i for i in range(0,len(ndvi),3)]
dates = [mean_ndvi['date'][i] for i in xtick]

plt.xticks(xtick,dates)

# 축 레이블 및 제목 설정
plt.xlabel('Date', fontsize=15)
plt.ylabel('Normalized value',fontsize=15)
plt.title('2016-2021_NDVI timeseries',fontsize=20, pad=15)
plt.grid(True, linestyle='--')

# plt.ylim(0,1)

# x축 레이블 회전
plt.xticks(rotation=45)
plt.legend()
plt.savefig(path+'mean_ndvimonthly_timeseries_2016_2021.png', dpi=300, bbox_inches='tight')
# 그래프 표시
plt.show()


import seaborn as sns
df = pd.DataFrame()
df['NDVI']            = ndvi
df['Drought']         = drou
df['Max temperature'] = temp
df['Precipitation']   = prec

corr = df.corr()
# corr2 = np.array(corr)

mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)]= True

fig = plt.subplots(figsize=(8,6))
plot = sns.heatmap(corr, 
                  xticklabels = corr.columns.values,
                  yticklabels = corr.columns.values,
                  mask = mask,
                  cmap = "bwr", 
                  vmin = -1, vmax = 1,
                  annot=True, fmt=".1f")
plt.title('Heatmap between variables')
plt.ylabel('Variables')
plt.savefig(path+'heatmap_all.png', dpi=300)
plt.show()
plt.close()
