from sklearn.preprocessing import StandardScaler
import numpy as np

def standardization(df, predict_num):
    '''평균0, 분산 1의 표준화. +volume은 차값을 이용.'''
    data_df = df[:-predict_num].copy()  # 요게 읽을 데이터.
    predict_df = df[-predict_num:].copy()  # 요게 정답레이블.

    # volume 정리.
    data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.

    scaler = StandardScaler()  # 스케일러 준비.
    scaler.fit(data_df)  # 스케일러 설정.
    data_df = scaler.transform(data_df)  # 스케일러 적용.
    predict_df = scaler.transform(predict_df)

    # df가 스케일러를 거치며 넘파이 배열로 바뀐다.

    return data_df, predict_df  # predict가 %로 나오지 않아 그 의미를 파악하기 어렵다는 단점이 있음.

def ohlc_normalizer(data_df):
    ### 공통 처리. ohlc 정규화
    last = data_df['close'].iloc[-1]
    data_df[['open', 'high', 'low', 'close']] = data_df[['open', 'high', 'low', 'close']] / last
    # high=low일 때를 대비해서 + 1e-8 를 넣으려 했으나... 시계열에서 있을 수 없는 일.
    return data_df


def normalizer_by_last_value(data_df):
    '''OHLCV를 받아 정규화한다. 모든 값을 마지막값으로 나누어, 상대적인 값으로.'''
    '''밖으론 OHLCV의 특성과 output으로 1개의 특성..'''


    data_df = ohlc_normalizer(data_df)  # 그냥 들어온 df 처리.

    # volume 정규화는.. 그냥 두어야 mfi 등 수치 계산에 좋다.
    ##### data_df volume 정규화
    # data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.
    # v_last = data_df['volume'].iloc[-1]
    # if v_last == 0:  # 몇몇 거래량 작은 것 중에 0이 나오는 경우가 있음.  # 요것도 몇으로 두는 게 적당할지 돌려보는 게 좋겠는데?
    #     pass
    # else:
    #     data_df['volume'] = data_df['volume'] / v_last
    ## 이건 다른 방식으로의 정규화.
    #scaler = StandardScaler()  # 스케일러 준비.
    #data_df['volume'] = scaler.fit_transform(data_df[['volume']])  # 스케일러 적용

    data_df.replace([np.inf, -np.inf], np.nan, inplace=True)  # 'inf'와 '-inf'를 NaN으로 대체. volume정보가 없는 경우 있음.
    data_df = data_df.dropna()  # 결측치가 생겨버린 가장 위의 행을 지워버린다.

    return data_df

def normalizer_1(df, window_num):
    '''OHLCV를 받아 정규화한다.'''
    '''밖으론 OHLCF의 특성과 output으로 1개의 특성..'''
    df = df.drop(columns='time')  # time 데이터를 날리고 사용할 것만 남긴다.
    data_df = df[:window_num].copy()  # 요게 읽을 데이터.
    predict_df = df[window_num:].copy()  # 요게 정답레이블.

    ### 공통 처리. ohlc 정규화
    high = data_df['high'].max()
    low = data_df['low'].min()
    data_df[['open', 'high', 'low', 'close']] = (data_df[['open', 'high', 'low', 'close']] - low) / (high-low)
    predict_df[['open', 'high', 'low', 'close']] = (predict_df[['open', 'high', 'low', 'close']] - low) / (high-low)
    # high=low일 때를 대비해서 + 1e-8 를 넣으려 했으나... 시계열에서 있을 수 없는 일.

    ### data_df 처리
    ##### data_df volume 정규화
    data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.
    v_high = data_df['volume'].max()
    v_low = data_df['volume'].min()
    data_df['volume'] = ( data_df['volume'] - v_low) / (v_high-v_low)
    data_df = data_df[4:]  # scinet 모델에 맞추기 위해 1496개만 사용한다.

    ##### 최종정리

    ### predict_df 처리.
    predict_df = predict_df[['open', 'high', 'low', 'close']]
    predict_df['mean'] = predict_df.mean(axis=1)  # 행 평균 구하기.
    ##### 최종정리
    predict_df = predict_df[['mean']]  # 사실상 의미있는 값만 남긴다.

    # 배열로 바꾼다.
    train_x_t = to_batch(data_df)
    train_y_t = to_batch(predict_df)

    return train_x_t, train_y_t



def regression_line(df):
    '''OHLCV를 받아 정규화한다.'''
    '''x에 대해 5개 특성, y에 대해 1개의 경향선만 나온다.'''
    df = df.drop(columns='time')  # time 데이터를 날리고 사용할 것만 남긴다.
    data_df = df[:1500].copy()  # 요게 읽을 데이터.
    predict_df = df[1500:].copy()  # 요게 정답레이블.

    ### 공통 처리. ohlc 정규화
    high = data_df['high'].max()
    low = data_df['low'].min()
    data_df[['open', 'high', 'low', 'close']] = (data_df[['open', 'high', 'low', 'close']] - low) / (high - low)
    predict_df[['open', 'high', 'low', 'close']] = (predict_df[['open', 'high', 'low', 'close']] - low) / (high - low)
    # high=low일 때를 대비해서 + 1e-8 를 넣으려 했으나... 시계열에서 있을 수 없는 일.

    ### data_df 처리
    ##### data_df volume 정규화
    data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.
    v_high = data_df['volume'].max()
    v_low = data_df['volume'].min()
    data_df['volume'] = (data_df['volume'] - v_low) / (v_high - v_low)
    data_df = data_df.dropna()  # 결측치가 생겨버린 가장 위의 행을 지워버린다.
    ##### 최종정리

    ### predict_df 처리.
    predict_df = predict_df[['open', 'high', 'low', 'close']]
    predict_df['mean'] = predict_df.mean(axis=1)  # 행 평균 구하기.
    ##### 최종정리
    predict_df = predict_df[['mean']]  # 사실상 의미있는 값만 남긴다.
    #회귀기울기를 찾아야 함.
    test = np.array(range(150))
    test = np.reshape(test, (150,))
    train_y = np.reshape(train_y, (150,))
    z = np.polyfit(test, train_y, 1)
    if z[0] > 0:
        predict_df = 1
    else:
        predict_df = 1

    # 배열로 바꾼다.
    train_x_t = to_batch(data_df)
    train_y_t = to_batch(predict_df)

    return train_x_t, train_y_t

def detect_10_percent(df, window_num):
    '''OHLCV를 받아 정규화한다.'''
    '''1500개 중 최고값이 몇인지 찾는다.'''
    df = df.drop(columns='time')  # time 데이터를 날리고 사용할 것만 남긴다.
    data_df = df[:window_num].copy()  # 요게 읽을 데이터.
    predict_df = df[window_num:].copy()  # 요게 정답레이블.

    ### 공통 처리. ohlc 정규화
    high = data_df['high'].max()
    low = data_df['low'].min()
    h_l = high - low
    last = data_df['close'].iloc[-1].copy()  # 마지막 값을 얻어둔다. 뒤의 변하는 비율을 구하기 위해.
    data_df[['open', 'high', 'low', 'close']] = (data_df[['open', 'high', 'low', 'close']] - low) / h_l
    # high=low일 때를 대비해서 + 1e-8 를 넣으려 했으나... 시계열에서 있을 수 없는 일.

    ### data_df 처리
    ##### data_df volume 정규화
    data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.
    v_high = data_df['volume'].max()
    v_low = data_df['volume'].min()
    data_df['volume'] = (data_df['volume'] - v_low) / (v_high - v_low)
    data_df = data_df.dropna()  # 결측치가 생겨버린 가장 위의 행을 지워버린다.
    ##### 최종정리

    ### predict_df 처리.
    predict_df = predict_df[['high']]  # 사실상 의미있는 값만 남긴다.
    max = predict_df.max()
    max = max[0]
    highst = max/last
    ##### 최종정리
    # ratio = last * 1.05
    # ratio_n = (ratio - low) / h_l
    # if max > ratio_n:
    #     predict_df = 1
    # else:
    #     predict_df = 0

    # 배열로 바꾼다.
    train_x_t = to_batch(data_df)
    train_y_t = np.array(highst)

    return train_x_t, train_y_t


def highst_value(df):
    '''OHLCV를 받아 정규화한다.'''
    '''2%를 넘는지 여부만 판별한다.'''
    df = df.drop(columns='time')  # time 데이터를 날리고 사용할 것만 남긴다.
    data_df = df[:1500].copy()  # 요게 읽을 데이터.
    predict_df = df[1500:].copy()  # 요게 정답레이블.

    ### 공통 처리. ohlc 정규화
    high = data_df['high'].max()
    low = data_df['low'].min()
    h_l = high - low
    data_df[['open', 'high', 'low', 'close']] = (data_df[['open', 'high', 'low', 'close']] - low) / h_l
    predict_df[['open', 'high', 'low', 'close']] = (predict_df[['open', 'high', 'low', 'close']] - low) / h_l
    # high=low일 때를 대비해서 + 1e-8 를 넣으려 했으나... 시계열에서 있을 수 없는 일.

    ### data_df 처리
    ##### data_df volume 정규화
    data_df['volume'] = data_df['volume'] - data_df['volume'].shift(1)  # 차값을 이용한다.
    v_high = data_df['volume'].max()
    v_low = data_df['volume'].min()
    data_df['volume'] = (data_df['volume'] - v_low) / (v_high - v_low)
    data_df = data_df.dropna()  # 결측치가 생겨버린 가장 위의 행을 지워버린다.
    ##### 최종정리

    ### predict_df 처리.
    predict_df = predict_df[['open', 'high', 'low', 'close']]
    predict_df['mean'] = predict_df.mean(axis=1)  # 행 평균 구하기.
    ##### 최종정리
    predict_df = predict_df[['mean']]  # 사실상 의미있는 값만 남긴다.
    max = predict_df.max()
    max = (max - low) / h_l

    # 배열로 바꾼다.
    train_x_t = to_batch(data_df)
    train_y_t = to_batch(max)

    return train_x_t, train_y_t