from datetime import datetime

from machine.machine import Machine
import day_observer
import time
from trade_info_machine import Trade_info_machine



class Downward_line():  # 하방선을 따라  진행하는 것을 구현하기 위한 클래스.
    def __init__(self):
        self.machine = Machine()  # 거래용 인스턴스를 만든다.
        self.interval = 86400  # 하루라면 86400초.
        self.ticker_list = self.machine.get_ticker_list()
        self.stop = {}  # 티커의 거래정지 시작시간을 정해두기 위한 사전.
        for ticker in self.ticker_list:
            self.stop[ticker] = 0
        # self.coin_DB = pymysql.connect(host='localhost', port=3306, db='coindb', user="root", passwd='vudghk99', charset='utf8')  # DB파일 연결을 위한 변수
        # self.cur = self.coin_DB.cursor()  # 커서 생성을 위한 변수
        print('하방선 전략. ready')
        self.trade_info_machine = Trade_info_machine()  # 정보저장용 클래스.

    def observe_downward_line(self, ticker, interval=1600):
        '''티커. 인터벌(분단위)를 받아 하강선을 검사한다.'''
        # print(ticker + '분석 start!')
        df = self.machine.get_candle_stick(order_currency=ticker, chart_intervals='1m')

        if df.shape[0] != 1500:  # 데이터가 충분히 있는 경우에만 진행한다.
            print(ticker)
            print(df)
            return print("데이터부족. 신생코인으로 사료됨.")
        else:
            mean = df['close'][780:].mean(axis=0)  # 주어진 데이터의 평균을 구한다.(하루 하고 1시간의 평균) => 1500개 중에 12시간치 720분.
            # 최근 기울기 검사.
            last = float(self.machine.get_current_price(ticker))  # 당장 현재 가격.
            ago_time = 30  # 약 30분 전의 데이터로.
            little_ago = df.iloc[-ago_time]['close']
            min = df['close'][-ago_time:].min(axis=0)  # ago_time 안에서 최소값.
            #- 여기서부터 판정
            if last <= mean * (1 - 0.02) and (last - min)/last > 0.003:  # 테스트. 빼보자.
            # 위에서 little_ago가 아니라... 가장 작은 값을 찾아야할 것 같네.
            #-- 현재 전략은 내가 원하는 지점을 잘 찾아낸다. 그러나, 전체적으로 하락세일 땐 어려운 전략이야.
                num_coin = 10000 / last
                a = self.machine.market_buy(currency=ticker, unit=num_coin)  # 가격이 달라졌을 수도 있으니..# 근데 현재 코인이 없어도 진행이 되나?
                print('가격은 ' + str(last) +str('.  ')+ str(datetime.today()))
                print(a)  # 구입 확인용.
                if a['status'] != '0000':
                    print('돈 모자라거나 뭔가 이상, 다음으로 패스.')
                    print('-------------절취선----------')
                else:
                    ### 팔기 전에 적당량이 구매되지 않았을 수 있다.
                    time.sleep(10)
                    price = last * (1 + 0.02)
                    print(str(price)+'에 판매 걸어둠.')
                    code = self.machine.limits_sell(currency=ticker, unit=num_coin, price=price)  # 거래를 실행하고 거래코드 반환.
                    code = code[2]  # 튜플의 3번째 요소가 'order_id'이다.
                    # self.trade_info_machine.save_order_id(code, ticker)  # 거래코드를 저장한다.
                    self.stop[ticker] = time.time() + 1800  # 거래정지 시간을 600초 더한다.(10분은 짧은 듯하여.. 30분으로 늘렸다.)
                    print('---------분리선-------')
        # print(ticker + '순회함', end="/")
    def observe_upward_line(self, ticker, interval=1600):
        '''티커. 인터벌(분단위)를 받아 상승선을 검사한다.'''
        pass

down = Downward_line()
ticker_list = down.ticker_list
target_list = ticker_list.copy()
danger_list = ["ARW", "SOC", "VELO", "MSB", "VRA", "SOC", "TRUE", "MSB", "BAKE", "IBP"]  # 위험요소.
db_added = False  # db에 최신정보 반영 여부.
for i in danger_list:
    try:  # 리스트에 없는 내용을 지우려니 에러가 나네;
        target_list.remove(i)  # 위험 요인들은 리스트에서 제거한다...(그럼 데이터를 못얻잖아? 그래서 리스트 카피.)
    except:
        pass
won = down.machine.total_value()  # 현재가치가 담기는 변수.
trade_info_machine = Trade_info_machine()
trade_info_machine.set_asset_won(won*1.05)  # 이 값 자체를 줄여서 많이 움직이게 하는 것도 방법이지.
target_won = trade_info_machine.show_asset_won()
####### 각 코인별 제한시간 걸어두는 장치 해두기.
print('순회 start')
def tour():
    global target_won, db_added
    while True:
        if db_added  == False:  # 스케쥴러가 믿음직스럽지 못해서...
            print('분 캔들 반영을 시작합니다.')
            observer = day_observer.Candle_info_machine()  # 정보를 얻는 인스턴스 생성.
            ticker_list = observer.machine.get_ticker_list()  # 티커리스트를 얻고,
            observer.add_ticker_stick(ticker_list=ticker_list)  # 정보를 db에 붙인다.
            db_added = True
        else:
            now = datetime.today()
            if (now.hour == 12) or (now.hour == 0):  # 하루 두 시간 정도는 정보를 얻자.
                db_added = False  # 각 12시가 되면 db 갱신을 해야함을 알린다.
        #print('여기까지 1순회' + str(datetime.today()))
        time.sleep(1)  # 1초 쉬지 않으면 이런저런 연산을 마구 넘길 때 API요청이 너무 많아진다.


        won = down.machine.total_value()  # 전체 자산을 새로이 계산.
        # if won > target_won:
        #     down.machine.cancle_all_order()  # 모든거래를 취소하고
        #     down.machine.selling_all()  # 모두 판다.
        #     trade_info_machine.reset_asset()  # won정보가 담긴 테이블을 비운다.
        #     trade_info_machine.set_asset_won(won * 1.05)  # 새로운 목표 설정.
        #     target_won = trade_info_machine.show_asset_won()


        for ticker in target_list:  # 주어진 리스트에 대해서만 순회한다.
            have = float(down.machine.balance()['data']['available_krw'])  # 현재 가용 가능한 금액.
            if have > 11000:
                if down.stop[ticker] < time.time():  # 저장된 시간이 현재시간보다 작다면 실행.
                    down.observe_downward_line(ticker=ticker)
            else:
                break


while 1:  # 에러가 반복나도 자동으로 실행되게끔.
    try:
        tour()
    except Exception as e:  # 에러가 나면 패스해서 재순회 하도록.
        for i in range(100):
            print(e)
        print(str(datetime.today()))
        print('------------------------------------------')
        pass
