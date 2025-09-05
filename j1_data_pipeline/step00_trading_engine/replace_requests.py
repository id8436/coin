'''학교 등에선 SSL 문제로 request 호출이 제대로 안되서... 우회하는 코드.'''
import requests
import json
from j0_personal_setting import secret

# 프록시 서버 주소 (필수!)
proxy_url = secret.proxy_server


def get(url, **kwargs):
    # GET 요청
    return request('GET', url, **kwargs)

def post(url, data=None, json=None, **kwargs):
    # POST 요청
    return request('POST', url, data=data, json=json, **kwargs)

# 필요하다면 PUT, DELETE 등 다른 HTTP 메소드도 추가

def request(method, url, **kwargs):
    # 1. 클라이언트가 요청한 정보를 프록시 서버가 알아들을 수 있는 형태로 만들기
    proxy_payload = {
        'target_url': url,           # 원래 요청하려던 URL
        'method': method,            # HTTP 메소드
        'params': kwargs.get('params', {}),   # GET 파라미터
        'headers': kwargs.get('headers', {}),  # 요청 헤더
        'data': kwargs.get('data'),           # POST/PUT 데이터 (폼 데이터)
        'json': kwargs.get('json'),           # POST/PUT 데이터 (JSON)
        # TODO: 필요하다면 다른 정보도 추가 (쿠키, 인증 정보 등)
    }

    # 2. 프록시 서버로 POST 요청 보내기
    # 여기서 발생하는 4xx/5xx 에러는 HTTPError로 raise_for_status()에서 발생
    response = requests.post(
        proxy_url,
        json=proxy_payload,
    )

    # 2xx 상태 코드가 아니면 requests.exceptions.HTTPError 발생
    # 이 예외는 이 함수를 호출한 곳(아래 if __name__ == '__main__': 블록)에서 잡을 것임
    response.raise_for_status()

    return response




if __name__ == '__main__':  # 테스트용 실행 블록.
    # 프록시 서버의 실제 주소를 여기에 정확히 입력해줘!
    proxy_server_url = "http://100.117.229.125:1991/requests/proxy_request/"

    # 테스트 데이터 (Post 요청 시 사용)
    post_data_json = {'key1': 'value1', 'key2': 123} # JSON 데이터
    post_data_form = {'key1': 'value1', 'key2': 456} # Form 데이터

    print(f"사용할 프록시 서버 주소: {proxy_server_url}\n")

    # 테스트 케이스 목록 정의
    test_cases = [
        ("GET 요청 테스트 (example.com)", "GET", "https://www.example.com", None, None),
        ("POST 요청 (JSON) 테스트 (httpbin.org/post)", "POST", "https://httpbin.org/post", None, post_data_json),
        ("POST 요청 (Form) 테스트 (httpbin.org/post)", "POST", "https://httpbin.org/post", post_data_form, None),
        # 필요한 경우 여기에 다른 테스트 URL 추가 (예: 금융사 API 주소)
        # ("금융사 API GET 테스트", "GET", "https://금융사_API_주소", None, None),
    ]

    for test_name, method, target_url, data_payload, json_payload in test_cases:
        print(f"=== {test_name} 시작 (대상 URL: {target_url}) ===")
        try:
            # ProxyRequests 클래스의 메소드 호출
            if method == "GET":
                 response = get(target_url)
            elif method == "POST":
                 response = post(target_url, data=data_payload, json=json_payload)
            # 필요한 경우 다른 메소드 추가

            # 성공했을 때 응답 출력
            print(f"  ✅ {test_name} 성공!")
            # 2xx 상태 코드인 경우만 이 아래 실행
            try:
                print("  응답 내용:", response.json())
            except json.JSONDecodeError:
                print("  응답 내용:", response.text)


        except requests.exceptions.RequestException as e:
            # requests 라이브러리 관련 에러 발생 시
            print(f"  ❌ {test_name} 실패: {e}")

            # === 여기서 프록시 서버 에러 응답 본문 출력 ===
            # 발생한 예외(e)가 HTTPError이고 응답 객체가 있는지 확인
            if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
                print("\n" + "=" * 40)
                print("!!! 프록시 서버에서 받은 상세 에러 응답 본문 !!!")
                print(f"  응답 상태 코드: {e.response.status_code}")
                print("=" * 40)
                try:
                    # 프록시 서버가 보낸 응답 본문을 JSON으로 파싱 시도
                    # ensure_ascii=False는 한글 깨짐 방지
                    error_body_json = e.response.json()
                    print(json.dumps(error_body_json, indent=4, ensure_ascii=False))
                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 텍스트 그대로 출력
                    print("응답 본문이 JSON 형식이 아님 (또는 파싱 오류):")
                    print(e.response.text)
                print("=" * 40 + "\n")

            else:
                 # HTTPError 외의 requests 에러 (예: 프록시 서버까지 연결 실패)
                 print("\n" + "-" * 40)
                 print("!!! 프록시 서버까지 도달하는 데 문제 발생 (HTTPError 아님) !!!")
                 print(f"  Requests 라이브러리 에러 타입: {type(e).__name__}")
                 print(f"  Requests 라이브러리 에러 메시지: {e}")
                 print("-" * 40 + "\n")


        except Exception as e:
             # 예상치 못한 다른 모든 에러
             print(f"  ❌ {test_name} 실행 중 예상치 못한 에러: {e}")

        print(f"=== {test_name} 종료 ===\n")


    # Optional: requests direct call test block
    # 이 블록은 회사망에서 requests로 외부 직접 접근 시 SSLError 나는지 확인용 (프록시와 무관)
    # print("=== requests 직접 호출 테스트 시작 (example.com - 회사망 SSLError 예상) ===")
    # try:
    #     res_direct = requests.get("https://www.example.com")
    #     print("  ✅ requests 직접 호출 응답:", res_direct)
    # except requests.exceptions.RequestException as e:
    #      print(f"  ❌ requests 직접 호출 실패 (예상): {e}")
    # print("=== requests 직접 호출 테스트 종료 ===\n")