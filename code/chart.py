import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# 1. CSV 파일 불러오기
dat = pd.read_csv('c:/temp/iowa22.csv')
# 2. 상관계수 행렬 계산 및 소수점 둘째 자리까지 반올림
cc = dat.corr()
cc = np.round(cc, 2)
print(cc)

# 3. 히트맵 그리기
ax = sb.heatmap(cc, cmap='coolwarm', linewidths=1, annot=True, fmt='.3f')
ax.xaxis.tick_bottom()
# 4. 제목 추가 및 이미지 저장
plt.title('Iowa State')
plt.savefig('c:/temp/iowa.png')
