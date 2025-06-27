import numpy as np


def mean_max(y):
    '''데이터를 받아 max의 평균을 뽑아낸다.'''
    # 기본적으로 3번째 행에 high가 있다.
    y = y[:, 3]
    y = np.mean(y)  # high들의 평균을 낸다.
    return y