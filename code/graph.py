import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#데이터 불러오기
dat = pd.read_csv('c:/temp/HH_VV.csv')
num = len(dat)
t = np.arange(0, num)
#HH, VV 데이터 추출
hh = dat['HH'].values
vv = dat['VV'].values
# 그래프 설정
fig, ax = plt.subplots(2, 1)
# 첫 번째 그래프: HH와 VV 시계열 비교
ax[0].plot(t, hh, label='HH', linewidth=0.5)
ax[0].plot(t, vv, label='VV', linewidth=0.5)
ax[0].set_xlabel('time')
ax[0].set_ylabel('Value')
ax[0].legend()
ax[0].grid(True)
# 두 번째 그래프: HH - VV 차이 시각화
diff = hh - vv
ax[1].plot(t, diff, color='black', linewidth=1)
ax[1].set_xlabel('time')
ax[1].set_ylabel('hh - vv')
ax[1].grid(True)

fig.tight_layout()
plt.savefig('c:/temp/HH_VV.png')
