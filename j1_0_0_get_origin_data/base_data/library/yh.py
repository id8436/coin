stock = yf.Ticker(code)
        current_price = stock.history(period='1d')['Close']
        shares_outstanding = stock.info['sharesOutstanding']  # 발행주수
        print(shares_outstanding)
        market_cap = current_price * shares_outstanding