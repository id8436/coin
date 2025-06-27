# 컨트롤 타워를 만들어보고 싶었어.
from trading_machine.bithumb.machine import Machine
import time
from datetime import datetime
import math
from trading_machine.bithumb import momentum  # 모멘텀 코드를 일단 가져온다.

###### 기초 준비. 전역변수.
bithumb = Machine()  # 클래스의 선언을 안해주면 클래스 내부 함수 실행에서 인자가 없다는 에러가 뜬다.
when = time.time()
asset_20 = float(bithumb.balance()['data']['available_krw']) * 0.2  # 현 자산의 20%



###-----------------작동
### 시작함수.



#------------동작
while 1:
    if when < math.floor(time.time()):  # 초단위로 1초마다 움직이게끔.
        when = time.time()
        # momonetum_observer()  # 모멘텀에 대한 검사 후 구매까지.

        today = datetime.today()
        if datetime.today().hour ==0 and datetime.today().minute == 0:  # if 자정이라면... 모든 걸 팔고 새로운 그... 타겟 찾기. 그리고 1분 쉬기.
            # momonetum_reset()
        else:
            pass