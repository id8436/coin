from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

User = 'id8436@naver.com'
User_target = 'user_id'  # id를 입력할 DOM요소 등을 지정.
Pass = 'Vudghk99$$'
Pass_target = 'user_pw'  # password를 입력할 DOM요소 등을 지정.
Pass2 = "2674"
Pass_target2 = 'payPassword'
url_login = "https://www.bithumb.com/member_operation/login"  # 로그인 페이지 주소.

browser: WebDriver = webdriver.Chrome(ChromeDriverManager().install())  # 이걸 브라우저로 사용한다.

browser.get(url_login)

target = browser.find_element_by_id(User_target)
target.clear()
target.send_keys(User)  # ID에 해당하는 내용 입력
target = browser.find_element_by_id(Pass_target)
target.clear()
target.send_keys(Pass)  # 비밀번호에 해당하는 내용 입력
# 버튼 누르기
form = browser.find_element_by_xpath('//*[@id="container"]/div[1]/div[5]/a')  # id와 password를 입력하고 제출버튼의 위치를 찾을 단서를 지정.
form.click()

browser.implicitly_wait(3)
target = browser.find_element_by_id(Pass_target2)
target.clear()
target.send_keys(Pass2)
form = browser.find_element_by_xpath('//*[@id="btnOK"]')
form.click()

browser.get("https://www.bithumb.com/asset_status/asset_my")
