import mpl_finance
import matplotlib.ticker as ticker
import pandas as pd


def candle_chart(canvas, df):
    mpl_finance.candlestick2_ohlc(canvas, df['start'], df['high'], df['low'], df['close'], width=0.5,
                                  colorup='r', colordown='b')
    canvas.legend(loc='best')  # 라벨 위치 설정
    canvas.grid(True)
    canvas.xaxis.set_major_locator(ticker.MaxNLocator(10))  # 요거 하면 x축이 정리가 되려나...?

def volume(canvas, df):
    color_fuc = lambda x: 'r' if x >= 0 else 'b'
    color_list = list(df['volume'].diff().fillna(0).apply(color_fuc))
    canvas.bar(df.index, df['volume'], width=0.5,
                     align='center',
                     color=color_list)

def prepare_volume_profile(df):
    '''매물대 그리기.'''
    unit_price = 1
    barrier = pd.DataFrame()  # 매물대 정보를 담을 df.
    # 최소단위부터 1씩 올라가며 가격대의 인덱스 생성.
    for price_range in range(int(df.close.min()), int(df.close.max()) + unit_price, unit_price):
        barrier.loc[price_range + unit_price / 2, 'volume'] = 0
    # 위와 같이 올라가며 인덱스에 내용 담기.
    for price_range in range(int(df.close.min()), int(df.close.max()) + unit_price, unit_price):
        index = (df.close >= price_range)  # 현재 조사하는 값보다 큰 경우만 찾고,
        index &= (df.close < price_range + unit_price)  # 현재 조사하는 값에 단위값을 더한 것보다 작은 것들과의 공통된 것만 담는다.
        # 즉, 해당 값 사이의 df.close의 인덱스가 얻어지는데, 이 인덱스에 해당하는 volume들의 값을 합해 저장한다.
        barrier.loc[price_range + unit_price / 2, 'volume'] += df[index].volume.sum()
    return barrier

def volume_profile(canvas, df):
    barrier = prepare_volume_profile(df)
    for i in range(0, len(barrier)):
        canvas.axhline(y=barrier.index[i], color='Orange', linestyle='-', linewidth=5, alpha=0.3, xmin=0,
                    xmax=barrier.iloc[i].volume / barrier.volume.max())

    canvas.axes.get_xaxis().set_visible(False)





def prepares(df, window_list):
    '''각종 지표를 만들기 위한 기초자료들을 모아둔 함수.'''
    # 최종가를 1로 두고...
    df[['start', 'high', 'low', 'close']] = df[['start', 'high', 'low', 'close']] / df['close'][-1] *100 # 최종가에 대해 비교하기 위해. +지지선을 잡기 위해 곱하기 100
    prepare_ma(df, window_list)
    prepare_mfi(df)
    prepare_macd(df)
    prepare_sonar(df)

def prepare_ma(df, window_list):
    for window in window_list:
        ma = df['close'].rolling(window=window).mean()
        col_name = str(window) + 'ma'
        df.insert(len(df.columns), col_name, ma)
def ma(canvas, df, window_list):
    line_list = ['solid', 'dashed', 'dotted', 'dashdot', 'solid']
    for i, window in enumerate(window_list):
        col_name = str(window) + 'ma'
        canvas.plot(df.index, df[col_name], label=col_name, linestyle=line_list[i])
    canvas.legend(loc='best')  # 라벨 위치 설정

def prepare_mfi(df):
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
def mfi(canvas, df):
    canvas.plot(df.index, df['MFI10'], label='MFI10')
    canvas.xaxis.set_major_locator(ticker.MaxNLocator(10))  # 요거 하면 x축이 정리가 되려나...?
    canvas.legend(loc='best')
    canvas.grid(True)
    canvas.xaxis.set_major_locator(ticker.MaxNLocator(10))

def prepare_macd(df):
    df['ma12'] = df['close'].rolling(window=12).mean()  # 12일 이동평균
    df['ma26'] = df['close'].rolling(window=26).mean()  # 26일 이동평균
    df['MACD'] = df['ma12'] - df['ma26']  # MACD
    df['MACD_Signal'] = df['MACD'].rolling(window=9).mean()  # MACD Signal(MACD 9일 이동평균)
    df['MACD_Oscil'] = df['MACD'] - df['MACD_Signal']  # MACD 오실레이터

def macd(canvas, df):
    canvas.plot(df.index, df['MACD'], label='MACD', color='r')
    canvas.plot(df.index, df['MACD_Signal'], label='MACD_Signal', color='g')
    canvas.bar(df.index, df['MACD_Oscil'], align='center', label='MACD_Oscil', width=0.5, color='orange')
    canvas.legend(loc='best')
    canvas.grid(True)
    canvas.xaxis.set_major_locator(ticker.MaxNLocator(10))

def prepare_sonar(df):
    df['sonar_ma'] = df['close'].rolling(window=10).mean()  # 이동평균
    df['sonar_ma_ago'] = df['close'].shift(9).rolling(window=10).mean()  # 9일 전의 이동평균
    df['sonar'] = df['sonar_ma'] - df['sonar_ma_ago']
    df['sonar_signal'] = df['sonar'].rolling(window=10).mean()
def sonar(canvas, df):
    canvas.plot(df.index, df['sonar'], label='sonar', color='r')
    canvas.plot(df.index, df['sonar_signal'], label='sonar_signal', color='b')
    canvas.legend(loc='best')
    canvas.grid(True)
    canvas.xaxis.set_major_locator(ticker.MaxNLocator(10))