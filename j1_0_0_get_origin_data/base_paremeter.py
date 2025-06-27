
## 세금 수수료 등은 자동 계산되니, test 머신에 직접 담는 건??
# 세금, 수수료 등 각종 기초 정보들을 담는다.

# data_machine에서 참고하는 값.
commission_rate = 0.0025  # 0.25%? 세금과 수수료. 러프하게 잡아봄.
fixed_commission = 1000  # 고정수수료 1000원?

# 시간 관련.(한국시간 기준)
korean_stock_market_open_time = '09:00:00'
korean_stock_market_close_time = '15:30:00'
us_stock_market_open_time = '11:30:00'  # 한국 시간 기준 미국 주식 시장 개장 시간
us_stock_market_close_time = '05:00:00'  # 한국 시간 기준 미국 주식 시장 종료 시간
frankfurt_stock_market_open_time_kst = '16:30:00'  # 유럽.
frankfurt_stock_market_close_time_kst = '23:00:00'
london_stock_market_open_time_kst = '17:00:00'  # 런던
london_stock_market_close_time_kst = '00:00:00'  # 다음 날
japan_stock_market_open_time = '09:00:00'
japan_stock_market_close_time = '15:00:00'
hong_kong_stock_market_open_time_kst = '10:00:00'
hong_kong_stock_market_close_time_kst = '16:00:00'
