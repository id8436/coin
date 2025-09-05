from j0_personal_setting import secret

# API 키 관련
bithumb_api_key = secret.bithumb_api_key
bithumb_api_secret = secret.bithumb_api_secret

# DB관련.
db_info = {
    'user': secret.db_user,
    'password': secret.db_password,
    'host': secret.db_host,
    'port': secret.db_port,
    'database': secret.db_name,
    'raise_on_warnings': secret.db_raise_on_warnings,
    'charset': secret.db_charset,
}
