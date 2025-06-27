import pandas as pd
import math
func_list = ['over_average_line', 'macd_score', 'mfi', 'volume_profile',
          'granville_signals']

# 이후 5일의 high 평균값을 냈을 때.
# 상관도는 100을 곱한 값이다.(너무 작은데...?)
parameter = {'macd_attenuation':1.8, 'macd_corr':3.68,  # log로 바꾸니... 0.028.나쁘지 않게 나오기도 함. 0.04대가 나오기도 하는데.. 사실상, 이 값 말곤... 이 값조차... 유의미하진 못한 듯하다.
             'over_average_line_attenuation':1.5,  # 매번 1 이하에 역상관계수가 나와; 신기한 일이네;
             # 아예 attenuation을 1 이상으로 잡고 상관도분석을 해보면 어떨까?
             'over_average_line_window':5, 'over_average_line_corr':1,  # window도 상관도 변형을 불러오진 못함.
             'mfi_corr':1,  # 0.009907 나왔었음. 0.06이 나오기도 함;;; 0.05, 0.02
             'volume_profile_corr':1.31,  # -0.02가 나오기도...
             'granville_signals_corr':2.3,  # -0.001이 나오기도.
             }

def macd_score(df):
    '''macd의 추세가 변하기 시작하는지 체크. 그걸 점수화 해서.'''
    # 기초 데이터 생성.(정석 생성방법과 조금 다른듯 하지만서도...)
    df = df.copy()  # 계산용 df는 따로 분리.
    # 아래는 단순 이동평균을 이용한 방식.
    # df['ma12'] = df['close'].rolling(window=12).mean()  # 12일 이동평균
    # df['ma26'] = df['close'].rolling(window=26).mean()  # 26일 이동평균
    # df['MACD'] = df['ma12'] - df['ma26']  # MACD
    # df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()  # MACD Signal(MACD 9일 이동평균)
    # df['MACD_Oscil'] = df['MACD'] - df['MACD_Signal']  # MACD 오실레이터

    # 아래는 지수 이동평균을 이용한 방식.
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()  # 12일 EMA
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()  # 26일 EMA
    df['MACD'] = df['ema12'] - df['ema26']  # MACD Line
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()  # Signal Line
    df['MACD_Oscil'] = df['MACD'] - df['MACD_Signal']  # MACD Histogram (Oscillator)

    for i in range(10):  # 0부터 9까지.  당장 오늘 것부터, 9일 전까지. 언제 꺾였는지도 반영하여 해당하는 점수를 준다.
        # 판단.
        last = df['MACD_Oscil'].iloc[-1-i]
        before = df['MACD_Oscil'].iloc[-2-i]
        before_2 = df['MACD_Oscil'].iloc[-3-i]
        # 요 차이가 클수록 변동이 심해질거라는 의미. 격차의 크기를 담기 위해서. 정규화가 되어 있다 가정.
        #score_base = score_base * 1  # 요 비례상수는 크기에 상관도 영향 없음. 너무 커지기도 하니 적당히 조절해보자.
        #score_base = abs(score_base)  # 로그가 음수를 받진 못하니까...
        #score_base = math.log(score_base)  # 밑이 10인 로그값으로 바꾸기.
        # 추세가 꺾일 때만 return 한다.
        print(f'의문인 점이 있어 check에서 살핀다. {last}, {before}')
        if (last > before) and (before < before_2) and (last < 0):  # 하향추세이다가 꺾이는 경우.
            # score_base = math.log(last- before)  # before - last  # 이렇게 했더니, 오히려 상향에서 꺾이는 경우를 가져오기도 함; 그냥 1로 두자.
            # score = score_base / (parameter['macd_attenuation'] ** i)  # 점수 저장.
            # return parameter['macd_corr'] * score
            return 1 / 2**i
        elif (last < before) and (before > before_2) and (last > 0):  # 상향추세이다가 걲이는 경우.
            return -1 / 2 ** i
        #    score = score_base / (parameter['macd_attenuation'] ** i)  # 점수 저장.
        #    return parameter['macd_corr'] * score
    return 0  # 아무것에도 해당하지 않으면 0.

def mfi(df):
    df = df.copy()  # 계산용 df는 따로 분리.
    df['PB'] = (df['close'] - df['low']) / (df['high'] - df['low'])
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3
    df['PMF'] = 0
    df['NMF'] = 0
    for i in range(len(df.close) - 1):
        if df.TP.values[i] < df.TP.values[i + 1]:
            df.PMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.NMF.values[i + 1] = 0
        else:
            df.NMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
            df.PMF.values[i + 1] = 0
    df['MFR'] = (df.PMF.rolling(window=10).sum() /
                 df.NMF.rolling(window=10).sum())
    df['MFI10'] = 100 - 100 / (1 + df['MFR'])

    return (df['MFI10'].iloc[-1] / 100) * parameter['mfi_corr']  # 총점이 1점이 되게 변형. +저평가될수록 높은 점수.

def over_average_line(df, window=5):
    '''직전에 평균선을 넘었는지 여부.'''
    df = df.copy()  # 계산용 df는 따로 분리.
    ma = df['close'].rolling(window=window).mean()
    col_name = 'average_line'
    df.insert(len(df.columns), col_name, ma)
    '''평균이동선 크로스 관찰.'''
    '''직전 안넘었는데, 지금 uni1이 uni2를 넘나 확인. 열 이름을 받아 작동한다.'''
    for i in range(10):
        if df['close'].iloc[-1-i] >= df['average_line'].iloc[-1-i] and df['close'].iloc[-2-i] <= df['average_line'].iloc[-2-i]:
            score = 1 / (parameter['over_average_line_attenuation'] ** i)
            return score * parameter['over_average_line_corr']
        elif df['close'].iloc[-1-i] <= df['average_line'].iloc[-1-i] and df['close'].iloc[-2-i] >= df['average_line'].iloc[-2-i]:
            score = -1 / (parameter['over_average_line_attenuation'] ** i)
            return score * parameter['over_average_line_corr']


def volume_profile(df):
    '''매물대 정보를 담을 데이터프레임 생성.'''
    # 들어온 df의 길이에 따라 매물대 형성 라인이 달라지니 유의.
    # %로 다루기 위해..
    df = df.copy()  # 계산용 df는 따로 분리.
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']] / df['close'].iloc[-1] * 100
    df[['volume']] = df[['volume']] / df['volume'].median() * 100  # 볼륨은 들쑥날쑥해서 중간값으로.
    unit_price = 1  # 1% 단위로 매물대를 그린다.
    barrier = pd.DataFrame()
    barrier_range = range(int(df.close.min()), int(df.close.max()) + unit_price, unit_price)
    for price_range in barrier_range:  # 기본 인덱스를 만든다.
        barrier.loc[price_range + unit_price / 2, 'volume'] = 0
    for price_range in barrier_range:
        index = (df.close >= price_range)
        index &= (df.close < price_range + unit_price)
        barrier.loc[price_range + unit_price / 2, 'volume'] += df[index].volume.sum()
    volume_profile_line_index = barrier.loc[barrier['volume'] == barrier['volume'].max()]  # 매물대 찾기.(%)
    volume_profile_line = volume_profile_line_index.index[0]  # 해당 인덱스에 해당하는 가격 가져오기.
    close = int(df['close'].iloc[-1])

    # 점수 계산: 'close' 값이 'volume_profile_line'을 얼마나 넘었는지 계산
    distance = close - volume_profile_line
    score = 1/distance  # 어차피 close=1로 맞추니까. / close  # 점수는 'distance'를 'unit_price'로 나눈 값으로 한다.

    return score * parameter['volume_profile_corr']

def granville_signals(df, window=20):
    '''그랜빌 매수, 매도신호 찾기.(뭔가 좀 이상하긴 하지만;;)'''
    df = df.copy()  # 계산용 df는 따로 분리.
    # 장기 이동평균선을 사용한다.
    # 이동평균선 계산
    df['moving_avg'] = df['close'].rolling(window=window).mean()
    # 저항선 계산 (여기서는 간단하게 최근 최고가로 설정)
    df['resistance'] = df['close'].rolling(window=window).max()

    # 매수/매도 신호 컬럼 초기화
    df['signal'] = 0

    # 매수 신호
    df.loc[(df['volume'] > df['volume'].shift(1)) & (df['close'] > df['close'].shift(1)) &
           (df['close'] > df['moving_avg']) & (df['close'] > df['resistance']), 'signal'] = 1

    # 매도 신호
    df.loc[(df['volume'] < df['volume'].shift(1)) & (df['close'] < df['close'].shift(1)) &
           (df['close'] < df['moving_avg']) & (df['close'] < df['resistance']), 'signal'] = -1
    score = df['signal'].iloc[-1]
    return score * parameter['granville_signals_corr']