import pybithumb
import time
import pandas
import sys#프로그램 종료를 위한 모듈.

#이 파일은.. 티커를 정한 후, 그 티커의 현재가를 계속 살피다가 타겟을 넘어가면 구매하는 프로그램이다.

con_key='0fd4afa676d607e30a9d1e8e36504cd4'#Connect Key
sec_key='a0c2799d8455873a328e5ee8508a2e6c'#Secret Key
bithumb=pybithumb.Bithumb(con_key,sec_key)#키를 넘겨 객체 생성
#원화잔고 확인
krw=bithumb.get_balance('BTC')[2]#왜 이런방식으로 잔고를 뽑아오는지 모르겠네;
#print(krw)#원화 보고 싶으면 주석 풀고.

#뭘 살지 찾기
df_max_benefit = pandas.read_excel('C:/Users/id843/PycharmProjects/coin/benefit_data.xlsx')#각 일수별 수익률 저장된 엑셀 불러오기.
df_max_benefit.sort_values(by='benefit10', ascending=False)#정렬해도 인덱스는 그대로다..ㅜ
index_5=df_max_benefit['benefit'].idxmax()#5일 최고가의 인덱스
index_10=df_max_benefit['benefit10'].idxmax()#10일 최고가의 인덱스
index_50=df_max_benefit['benefit50'].idxmax()#50일 최고가의 인덱스
ticker_5=df_max_benefit['Unnamed: 0'][index_5]#5일 최고가의 티커
ticker_10=df_max_benefit['Unnamed: 0'][index_10]#10일 최고가의 티커
ticker_50=df_max_benefit['Unnamed: 0'][index_50]#50일 최고가의 티커
#티커의 정보 불러오기
df_5=pybithumb.get_candlestick(ticker_5)
open_5=float(df_5['open'][-1])
high_5=float(df_5['high'][-2])
low_5=float(df_5['low'][-2])
v_5=float(df_max_benefit['max_v'][index_5])
target_5=round(open_5 + (high_5 - low_5)*v_5,1)
#10일짜리
df_10=pybithumb.get_candlestick(ticker_10)
open_10=float(df_10['open'][-1])
high_10=float(df_10['high'][-2])
low_10=float(df_10['low'][-2])
v_10=float(df_max_benefit['10v'][index_10])
target_10=open_10 + (high_10 - low_5)*v_10
#50일짜리
df_50=pybithumb.get_candlestick(ticker_50)
open_50=float(df_50['open'][-1])
high_50=float(df_50['high'][-2])
low_50=float(df_50['low'][-2])
v_50=float(df_max_benefit['50v'][index_50])
target_50=open_50 + (high_50 - low_5)*v_50

buy_5=krw*0.997
#여기..연습해둬야 겠다; 왜 오류가 나는지 모르겠네; 주문규약을 알아야 해. 1000원단위인가? 최소구매단위를 알아야 해.
count_5 = round(buy_5 / target_5,4)#target_5와 함께 소수점규약을 알아야겠어.

while 1:
    all = pybithumb.get_current_price("ALL")
    current_5 = float(all[ticker_5]['closing_price'])#모든 값 중에 ticker_5의 현재가만 골라낸다.
    # 주문 후, 주문번호를 담고 저장.
    pay_list = []  # 주문번호를 담아둘 리스트.
    if current_5 >= target_5:#현재가가 타겟을 넘어가면 발동
        try:
            order_5 = bithumb.buy_market_order(ticker_5, count_5)#구입!
            pay_list.append(order_5)
            print(order_5)# 이게 있어야 구매가 됬는지, 안됬는지 알 수 있다.
            #튜플을 저장해야 하는데, 그게 안되니까...ㅜ
            a=str(order_5[0])
            b=str(order_5[1])
            c=str(order_5[2])
            d=str(order_5[3])
            e=a+','+b+','+c+','+d+'\n'
            text = open('C:/Users/id843/PycharmProjects/coin/order.txt', 'at')
            text.write(e)#주문번호 저장
            text.close()
            sys.exit()
        except:
            pass

    term=0.1#함수를 불러올 시간간격
    time.sleep(term)
