import math

class OrderUnitAdjuster:
    def __init__(self, price_unit_rules, coin_unit_rules, min_order_amount):
        """
        Args:
            price_unit_rules (dict): 가격에 따른 최소 호가 단위 규칙
            coin_unit_rules (dict): 가격에 따른 최소 주문 수량 규칙
        """
        self.price_unit_rules = price_unit_rules
        self.coin_unit_rules = coin_unit_rules
        self.min_order_amount = min_order_amount

    def adjust_price(self, current):
        """가격(current)을 최소 호가 단위에 맞춰 조정"""
        for price_range, unit in self.price_unit_rules.items():
            min_price, max_price = price_range
            if min_price <= current < max_price:
                price_unit = unit
                break
        else:  # 가격이 어떤 범위에도 해당하지 않는 경우
            price_unit = min(self.price_unit_rules.values())  # 최소 단위로 설정

        current = float(current)
        current = round(current, price_unit)
        if current > self.min_order_amount:
            current = int(current)
        return current

    def adjust_quantity(self, num_coin, current):
        """수량(num_coin)을 최소 주문 단위에 맞춰 조정. 현재가에 따라 갯수가 달라짐."""
        for price_range, unit in self.coin_unit_rules.items():
            min_price, max_price = price_range
            if min_price <= current < max_price:  # num_coin 기준으로 변경
                coin_unit = unit
                break
        else:  # 가격이 어떤 범위에도 해당하지 않는 경우
            coin_unit = min(self.coin_unit_rules.values())  # 최소 단위로 설정

        num_coin = float(num_coin)
        num_coin = num_coin * (10 ** coin_unit)  # 내림을 적용하기 위함
        num_coin = math.floor(num_coin)  # 내림 적용
        num_coin = num_coin * (10 ** -coin_unit)  # 되돌리기
        num_coin = round(num_coin, coin_unit)  # 소수점을 잘라줘 거래가 가능한 양으로 맞춘다
        return num_coin

    def set_unit(self, num_coin, current=0):
        """최소 호가 단위와 최소 구매 단위에 맞추기"""
        current = self.adjust_price(current)
        num_coin = self.adjust_quantity(num_coin, current)

        if current * num_coin < self.min_order_amount:
            print(f'최소주문금액({self.min_order_amount})에 미치지 못함.')
            print("조정된 가격:", current)
            print("조정된 수량:", num_coin)
            print(f"총 구매 시도액:{current * num_coin}")
        return current, num_coin





if __name__ == '__main__':  # 테스트용.
    # 규칙 정의 (가격 범위: 최소 단위)
    # 빗썸의 경우 https://www.bithumb.com/customer_support/info_guide/info-guide/536 에 있음.
    price_unit_rules = {
        (0, 1): 4,  # 1원 이상일 때는 소수점 4자리까지 살림.
        (1, 10): 3,
        (10, 100): 2,
        (100, 1000): 1,
        (1000, 5000): 0,
        (5000, 10000): -2,
        (10000, 50000): -2,
        (50000, 100000): -3,
        (100000, 500000): -3,
        (500000, 1000000): -4,
        (1000000, float('inf')): -4,
    }

    coin_unit_rules = {
        (0, 100): -1,  # 개당 100원이 안되면 10개부터 주문 가능.
        (100, 1000): 0,
        (1000, 10000): 1,
        (10000, 100000): 2,
        (100000, 1000000): 3,
        (1000000, float('inf')): 4,
    }

    # 클래스 인스턴스 생성
    adjuster = OrderUnitAdjuster(price_unit_rules, coin_unit_rules, min_order_amount=5000)

    # 가격, 수량 조정
    current_price = 1000  # 현재 가격
    num_coin = 12.345    # 구매 수량
    adjusted_price, adjusted_quantity = adjuster.set_unit(num_coin, current_price)

    print("조정된 가격:", adjusted_price)       # 조정된 가격: 55500
    print("조정된 수량:", adjusted_quantity)    # 조정된 수량: 0.12

