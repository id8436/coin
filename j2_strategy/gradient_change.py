# interval=self.batch, recent_check_interval=30, weight=0.02, target_price=0.02
''' 그리드 예시.
param_grid = {
    'param1': [20, 30, 40, 50],
    'param2': [10, 20, 30, 40, 50],
    'param3': [0.005, 0.01, 0.015, 0.02, 0.0025],
    'param4': [0.005, 0.01, 0.015, 0.02, 0.0025],
}
'''
def lowerThanMean_PlusGradient(data_df, restore_info, **params):
    '''인터벌 사이의 평균값보다 낮고, 최근 기울기가 상승세를 그리기 시작할 때 구매.'''
    # 설명.
    ''' 받는 것은 마지막 값을 1로 규격화 한 df.'''
    '''# 기초 파라미터
    interval: 얼마동안의 데이터를 볼 것인가. 인덱스로. 30 정도?
    recent_check_interval: 중간 판단지점을 어느 정도로 할 것인가. 5 정도??
    weight: 어느 가중치로 둘 것인가. 0.0002 정도? 인터벌과 엮여서...
    target_price: 얼마만큼의 비율을 판매가로 잡을 것인가. 0.02 정도?
    '''
    interval = params.get('param1')
    recent_check_interval = params.get('param2')
    weight = params.get('param3')
    target_price = params.get('param4')

    # 논리의 재료들.
    mean_price = 0  # 평균가를 담기 위한 변수
    current = data_df.iloc[-1]['close']
    last = data_df.iloc[-recent_check_interval ]['close']
    little_ago = data_df.iloc[-interval]['close']

    # 일정 구간으로부터의 평균.
    mean_price = data_df.iloc[-interval:]['close'].mean()
    # 중간지점까지의 기울기 구하기
    # grad = (last - little_ago) / interval
    recent_grad = (current - last) / recent_check_interval
    if current <= mean_price * (1 - weight):
        if recent_grad > 0:
        # if grad < 0 and (current - little_ago) > 0:
            target_price = float((target_price +1) * restore_info)  # 기본적으로 퍼센테이지로 드러냄.
            how_many = 6000 / target_price  # 숫자를 기본 구매가격으로.(25년 기준 빗썸 최소가 5천원이라)
            return True, target_price, how_many
    return False, None, None

