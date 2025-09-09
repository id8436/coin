"""
KIS trading engine (한국투자증권 거래 엔진)
- OAuth2 토큰 발급/갱신
- 공통 요청 헬퍼
- 샘플 시세 조회 메소드(inquire_price)

주의:
- 네트워크 환경(학교 등)에서는 SSL 이슈 때문에 replace_requests 래퍼를 사용합니다.
- 실제 주문 시에는 tr_id, 계좌정보(계좌번호 등)와 매체인증 설정이 필요합니다. 본 파일은 최소한의 골격을 제공합니다.
"""
from typing import Optional, Dict, Any
import time
from j0_personal_setting import secret
from j1_data_pipeline.step00_trading_engine import replace_requests as requests


class Machine:
    """한국투자증권 거래머신 (Minimal)

    Parameters
    - appkey/appsecret: secret.py에 기본값이 있어 생략 가능
    - paper: True이면 모의투자(VTS) 서버, False이면 실서버
    - timeout: 요청 타임아웃(초)
    """

    def __init__(
        self,
        appkey: Optional[str] = None,
        appsecret: Optional[str] = None,
        paper: bool = True,
        timeout: int = 15,
    ) -> None:
        self.appkey = appkey or getattr(secret, "KIS_API_Key", None)
        self.appsecret = appsecret or getattr(secret, "KIS_API_Secret", None)
        if not self.appkey or not self.appsecret:
            raise ValueError("KIS appkey/appsecret not found. Please set in secret.py or pass as arguments.")

        # KIS 서버 주소
        self.base_url = (
            "https://openapivts.koreainvestment.com:29443" if paper else "https://openapi.koreainvestment.com:9443"
        )
        self.timeout = timeout

        # OAuth 토큰 캐시
        self._access_token: Optional[str] = None
        self._token_expiry_ts: float = 0.0

    # ----------------------- Token -----------------------
    def _token_valid(self) -> bool:
        return bool(self._access_token) and (time.time() < self._token_expiry_ts - 30)

    def authenticate(self) -> str:
        """유효 토큰을 보장하고 토큰 문자열을 반환"""
        if not self._token_valid():
            self._fetch_token()
        assert self._access_token
        return self._access_token

    def _fetch_token(self) -> None:
        """OAuth2 Client Credentials로 토큰 발급"""
        url = f"{self.base_url}/oauth2/v1/token?grant_type=client_credentials"
        headers = {
            "content-type": "application/json; charset=utf-8",
            "appkey": self.appkey,
            "appsecret": self.appsecret,
        }
        payload = {"grant_type": "client_credentials"}
        res = requests.post(url, json=payload, headers=headers)
        data = {}
        try:
            data = res.json()
        except Exception:
            # 프록시 오류 등으로 JSON이 아닐 수 있음
            raise RuntimeError(f"Token response not JSON: {getattr(res, 'text', '')}")

        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 0)
        if not access_token:
            raise RuntimeError(f"Failed to fetch token: {data}")

        self._access_token = access_token
        # 유효기간(초). 약간의 여유를 두고 만료처리
        try:
            expires_sec = int(expires_in)
        except Exception:
            expires_sec = 3600
        self._token_expiry_ts = time.time() + max(30, expires_sec - 30)

    # ----------------------- Generic request -----------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        needs_auth: bool = True,
    ):
        """KIS REST 공통 요청
        - path: '/uapi/...' 처럼 슬래시로 시작하는 경로
        - headers: 필요 시 tr_id, custtype 등 추가 가능
        """
        if not path.startswith('/'):
            path = '/' + path
        url = f"{self.base_url}{path}"

        base_headers = {
            "content-type": "application/json; charset=utf-8",
            "appkey": self.appkey,
            "appsecret": self.appsecret,
        }
        if needs_auth:
            base_headers["authorization"] = f"Bearer {self.authenticate()}"
        if headers:
            base_headers.update(headers)

        m = (method or "").upper()
        if m == "GET":
            return requests.get(url, headers=base_headers, params=params)
        elif m in ("POST", "PUT", "DELETE", "PATCH"):
            # replace_requests는 method별 래퍼가 GET/POST만 있으므로 POST에 data/json만 사용
            return requests.post(url, headers=base_headers, params=params, json=json, data=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

    # ----------------------- Sample API -----------------------
    def inquire_price(self, code: str, market_div: str = "J"):
        """국내주식 현재가 조회 (샘플)
        - code: 종목코드 6자리 (예: '005930')
        - market_div: 'J' (주식) 등
        주의: tr_id는 상황에 따라 다를 수 있음. 일반적으로 'FHKST01010100'가 사용됩니다.
        """
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        params = {
            "fid_cond_mrkt_div_code": market_div,
            "fid_input_iscd": code,
        }
        headers = {
            "tr_id": "FHKST01010100",
        }
        return self.request("GET", path, headers=headers, params=params)