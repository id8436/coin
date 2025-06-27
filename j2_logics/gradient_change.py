
def lowerThanMean_PlusGradient(data_df, interval, recent_check_interval , weight):
    '''인터벌 사이의 평균값보다 낮고, 최근 기울기가 상승세를 그리기 시작할 때 구매.'''
    # 설명.
    ''' 받는 것은 마지막 값을 1로 규격화 한 df.'''
    '''# 기초 파라미터
    interval: 얼마동안의 데이터를 볼 것인가. 인덱스로. 30 정도?
    recent_check_interval: 중간 판단지점을 어느 정도로 할 것인가. 5 정도??
    weight: 어느 가중치로 둘 것인가. 0.0002 정도? 인터벌과 엮여서...
    '''

    # 논리의 재료들.
    mean_price = 0  # 평균가를 담기 위한 변수
    current = data_df[-1][0]
    last = data_df[-recent_check_interval ][0]
    little_ago = data_df[-interval][0]

    # 일정 구간으로부터의 평균.
    mean_price = data[-interval:][0].mean()
    # 중간지점까지의 기울기 구하기
    grad = (last - little_ago) / interval
    recent_grad = (current - data_df[-middle_interval][0]) / middle_interval
    if current <= mean_price * (1 - weight * interval):  # 인터벌이 커질수록 더 크게 하락된 지점을 찾게끔.
        if recent_grad > 0:
        # if grad < 0 and (current - little_ago) > 0:
            print(lowerThanMean_PlusGradient)
            return True

if __name__ == "__main__":
    from j1_0_0_get_origin_data.base_data_machine import InfoMachine
    info_machine = InfoMachine(asset_type="stock", market_codes=['KOSDAQ'])
    base_df = info_machine.get_price_df(interval='24h', code='196170', payment_currency='KRW', data_from='2024-10-3')

    print(do_df)