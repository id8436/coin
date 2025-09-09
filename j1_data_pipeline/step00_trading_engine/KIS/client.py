"""
KIS high-level client (한국투자증권 편의용 클라이언트)
- Machine 위에 얹는 간단한 래퍼로, 보다 쉬운 메소드 제공
- 기본값은 안전하게: paper=True(모의투자), dry_run=True(주문 미전송)

주의:
- 실제 주문 시에는 계좌번호(CANO)와 상품코드(ACNT_PRDT_CD='01' 등) 설정이 정확해야 합니다.
- 본 클라이언트는 최소 동작 예시이며, KIS 문서를 반드시 확인하세요.
"""
from __future__ import annotations
from typing import Optional, Dict, Any

from j0_personal_setting import secret
from .machine import Machine


class Client:
    """한국투자증권 클라이언트 (편의 래퍼)

    Parameters
    - cano: 계좌번호(앞 8자리). secret.KIS_CANO 가 있으면 기본값 사용
    - acnt_prdt_cd: 계좌상품코드(보통 '01'). secret.KIS_ACNT_PRDT_CD 있으면 기본값 사용
    - paper: 모의투자 여부(True=모의)
    - dry_run: True면 주문 API를 실제로 호출하지 않고 payload만 반환
    - appkey/appsecret: secret에 없으면 직접 전달
    """

    def __init__(
        self,
        *,
        cano: Optional[str] = None,
        acnt_prdt_cd: Optional[str] = None,
        paper: bool = True,
        dry_run: bool = True,
        appkey: Optional[str] = None,
        appsecret: Optional[str] = None,
    ) -> None:
        self.paper = paper
        self.dry_run = dry_run
        # 비밀키는 Machine이 secret에서 읽어오게 둠 (필요시 덮어쓰기)
        self.machine = Machine(appkey=appkey, appsecret=appsecret, paper=paper)

        # 계좌 정보: secret에 있으면 활용
        self.cano = cano or getattr(secret, "KIS_CANO", None) or ""
        self.acnt_prdt_cd = acnt_prdt_cd or getattr(secret, "KIS_ACNT_PRDT_CD", None) or "01"

    # ----------------------- 조회 편의 -----------------------
    def price(self, code: str, market_div: str = "J") -> Optional[float]:
        """현재가를 float로 반환 (없으면 None)
        - code: 종목코드 6자리
        - market_div: 기본 'J' (주식)
        """
        res = self.machine.inquire_price(code, market_div=market_div)
        try:
            data = res.json()
        except Exception:
            return None
        # 응답 스키마: output에 PRPR(현재가) 존재 (문자형)
        try:
            output = data.get("output") or {}
            prpr = output.get("prpr")  # 문자열 가격
            return float(prpr.replace(",", "")) if prpr is not None else None
        except Exception:
            return None

    # ----------------------- 주문 편의 -----------------------
    def order_cash(
        self,
        *,
        code: str,
        qty: int,
        price: Optional[float] = None,
        side: str = "BUY",
        ord_dvsn: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """현금주문 (시장가/지정가)
        - code: 종목코드
        - qty: 수량(정수)
        - price: 지정가일 때 가격. None이면 시장가
        - side: 'BUY' 또는 'SELL'
        - ord_dvsn: KIS 주문구분 코드(모르면 None). None일 때는 기본값 적용
          (기본값: 시장가='01', 지정가='00')
        - extra: 추가로 body에 합칠 키-값(dict)
        반환: dry_run=True면 (url, headers, body) 튜플을 반환. False면 requests.Response
        """
        if not self.cano:
            raise ValueError("계좌번호(cano)가 필요합니다. Client(cano=...) 또는 secret.KIS_CANO 설정")

        side_u = (side or "").upper()
        if side_u not in ("BUY", "SELL"):
            raise ValueError("side must be 'BUY' or 'SELL'")

        is_market = price is None
        # 기본 주문구분 코드 (KIS 문서 기준 예시)
        # - '00': 지정가, '01': 시장가 (문서/환경에 따라 다를 수 있으니 반드시 확인)
        if ord_dvsn is None:
            ord_dvsn = "01" if is_market else "00"

        # 모의/실서버 tr_id 매핑 (KIS 예시)
        # - 현금 매수: (모의) VTTC0802U, (실) TTTC0802U
        # - 현금 매도: (모의) VTTC0801U, (실) TTTC0801U
        if self.paper:
            tr_id = "VTTC0802U" if side_u == "BUY" else "VTTC0801U"
        else:
            tr_id = "TTTC0802U" if side_u == "BUY" else "TTTC0801U"

        path = "/uapi/domestic-stock/v1/trading/order-cash"
        headers = {
            "tr_id": tr_id,
            "custtype": "P",  # 개인
        }
        body: Dict[str, Any] = {
            "CANO": self.cano,
            "ACNT_PRDT_CD": self.acnt_prdt_cd,
            "PDNO": code,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": str(int(qty)),
            # 가격: 시장가일 때는 보통 '0' 또는 빈값 처리 (문서 확인 필수)
            "ORD_UNPR": "0" if is_market else str(price),
        }
        if extra:
            body.update(extra)

        if self.dry_run:
            # 실제 호출 없이 확인용으로 반환
            return (path, headers, body)

        return self.machine.request(
            "POST",
            path,
            headers=headers,
            json=body,
            params=None,
            needs_auth=True,
        )

    def order_cash_buy(self, code: str, qty: int, price: Optional[float] = None, ord_dvsn: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        """현금 매수 편의 메소드"""
        return self.order_cash(code=code, qty=qty, price=price, side="BUY", ord_dvsn=ord_dvsn, extra=extra)

    def order_cash_sell(self, code: str, qty: int, price: Optional[float] = None, ord_dvsn: Optional[str] = None, extra: Optional[Dict[str, Any]] = None):
        """현금 매도 편의 메소드"""
        return self.order_cash(code=code, qty=qty, price=price, side="SELL", ord_dvsn=ord_dvsn, extra=extra)

    # ----------------------- 저수준 유틸 -----------------------
    def raw(self, method: str, path: str, **kwargs):
        """Machine.request를 그대로 노출 (유연성 제공)"""
        return self.machine.request(method, path, **kwargs)


__all__ = ["Client"]
