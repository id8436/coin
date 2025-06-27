import sys
from xcoin_api_client import *


api_key = "0fd4afa676d607e30a9d1e8e36504cd4";
api_secret = "a0c2799d8455873a328e5ee8508a2e6c";

api = XCoinAPI(api_key, api_secret);

rgParams = {
	"order_currency" : "BTC",
	"payment_currency" : "KRW"
};


#
# public api
#
# /public/ticker
# /public/recent_ticker
# /public/orderbook
# /public/recent_transactions

result = api.xcoinApiCall("/public/ticker", rgParams);
print("status: " + result["status"]);
print("last: " + result["data"]["closing_price"]);
print("buy: " + result["data"]["min_price"]);


#
# private api
#
# endpoint		=> parameters
# /info/current
# /info/account
# /info/balance
# /info/wallet_address

#result = api.xcoinApiCall("/info/account", rgParams);
#print("status: " + result["status"]);
#print("created: " + result["data"]["created"]);
#print("account id: " + result["data"]["account_id"]);
#print("trade fee: " + result["data"]["trade_fee"]);
#print("balance: " + result["data"]["balance"]);

sys.exit(0);