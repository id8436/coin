from machine.machine import Machine
import pandas as pd
import time  # 쌩 데이터가 들어오기 때문에 보기 좋게 바꾸기 위함.
import os  # 저장경로를 지정하기 위함.

machine = Machine()

def make_excel(chart_intervals='24h', order_currency="BTC"):
    data = machine.get_candle_stick(chart_intervals=chart_intervals, order_currency=order_currency)
    df = pd.DataFrame(data)  # 가져온 데이터를 df화.
    df.rename(columns={0:'time',1:"시가", 2:"종가", 3:"고가",4:"저가",5:"거래량"}, inplace=True)  # 목차를 바꾸어준다.
    df.sort_values('time', inplace=True)  # 시간순서가 뒤바뀔 수 있기에 데이터 정렬.
    wd = os.getcwd()  # 현재 디랙터리.
    file_dir = '{}\\candle\\'.format(wd)  # 저장할 경로.
    file_name = 'candle_interval{}_about{}.xlsx'.format(chart_intervals, order_currency)
    df.to_excel(file_dir + file_name)  # 파일저장.

import pybithumb
def make_candle_all(chart_intervals='24h'):
    tickers = pybithumb.get_tickers()
    for ticker in tickers:
        make_excel(chart_intervals=chart_intervals, order_currency=ticker)
        print(ticker+" done")

make_candle_all()