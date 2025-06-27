import requests

login_url = 'https://www.bithumb.com/member_operation/checkLoginFailBlock?_=1618002677635'
login_info = {'usrId':'id8436',
        'loginType':'email',
        'csrf_xcoin_name':'eda4f8004afe038ab1402f097dd174ea',
        }

res = requests.get("http://id8436.iptime.org:2786/mediawiki/index.php/Requests")
print(res)

session = requests.session()

res = session.post(login_url, data=login_info)  # 위에서 작성한 내용을 Post 방식으로 요청하고 응답받는다.
res.raise_for_statue()  # 오류가 발생하면 에러를 반환하게 한다.

print(res.raise_for_status())

print(res.text)