import pandas as pd

from alart_info import get_candle_stick, get_ticker_list
import numpy as np
have_money = 1000  # 천원으로 시작.
have_coin = 0
window_list = [1, 5, 10, 20, 60]
how_long = 100
import random

def filter_1unit_over_5unit(ticker):
    df = get_candle_stick(chart_intervals='24h', order_currency=ticker, payment_currency="KRW")

    for window in window_list:
        ma = df['close'].rolling(window=window).mean()
        col_name = str(window) + 'unit'
        df.insert(len(df.columns), col_name, ma)
    df = df[-how_long:-1]
    df['over_5unit'] = np.where(df['close']>df['5unit'], 1, 0)
    pd.set_option('display.max_columns', None)
    print(len(df))
    print(df)
    pre_1unit_over = 0  # 이전 값에서 넘었는지 여부.
    perchace_price = 0  # 구입한 가격.
    perchaced = False  # 샀는지 여부.
    for i in range(len(df)):
        if df['over_5unit'][i] > pre_1unit_over:
            buy_price = random.randint(int(df['close'][i]), int(df['high'][i]))
            print(df.index[i])
            buy(buy_price)
            perchaced = True
        if pre_1unit_over > df['over_5unit'][i]:
            sell_price = random.randint(int(df['low'][i]), int(df['close'][i]))
            print(df.index[i])
            sell(sell_price)
            perchaced =False
        pre_1unit_over = df['over_5unit'][i]

def filter_buy_5unit_sell_102(ticker):
    df = get_candle_stick(chart_intervals='24h', order_currency=ticker, payment_currency="KRW")

    for window in window_list:
        ma = df['close'].rolling(window=window).mean()
        col_name = str(window) + 'unit'
        df.insert(len(df.columns), col_name, ma)
    df = df[-how_long:-1]
    df['over_5unit'] = np.where(df['close']>df['5unit'], 1, 0)
    pd.set_option('display.max_columns', None)
    print(len(df))
    print(df)
    pre_1unit_over = 0  # 이전 값에서 넘었는지 여부.
    perchace_price = 0  # 구입한 가격.
    perchaced = False  # 샀는지 여부.
    for i in range(len(df)):
        if df['over_5unit'][i] > pre_1unit_over:
            if perchaced:
                continue
            else:
                pass
            buy_price = random.randint(int(df['close'][i]), int(df['high'][i]))
            print(df.index[i])
            buy(buy_price)
            perchace_price = buy_price
            perchaced = True
        if df['high'][i] > perchace_price*1.02 and perchaced:
            sell_price = perchace_price*1.02 #random.randint(int(df['start'][i]), int(df['high'][i]))
            print(df.index[i])
            sell(sell_price)
            perchaced =False
        pre_1unit_over = df['over_5unit'][i]

def buy(price):
    global have_coin, have_money
    money = have_money * 0.9975  # 만약 구매기회가 또 와도 가진 돈이 0이면 사는 게 없겠지.
    have_coin = have_coin + (money / price)  # 구매할 코인 갯수. 이만큼 갖게 된다.
    have_money = 0  # 다 샀다고 가정하면 0.
    print('삼!!! 가진 돈 : ' + str(have_money) + ', 가진 코인 갯수 : ' + str(have_coin) + ' 얼마에? : ' + str(price) )
def sell(price):
    global have_coin, have_money
    have_coin = have_coin * 0.9975
    have_money = have_money + (have_coin * price)
    have_coin = 0
    print('팜!!! 가진 돈 : ' + str(have_money) + ', 가진 코인 갯수 : ' + str(have_coin) + ' 얼마에? : ' + str(price))


filter_buy_5unit_sell_102('BTC')