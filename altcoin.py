import time
import pyupbit
import datetime

access = "UjNMD0uPVT96zw2n3u4im1BFKefDcGeWMNPXbsil"
secret = "wPtSlvDpoBzZJMxyHkgGKvOFzzYf8puUPodWZvFj"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-STORJ")
        end_time = start_time + datetime.timedelta(days=1)

        # 9:00 < 현재 < 8:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-STORJ", 0.3)
            current_price = get_current_price("KRW-STORJ")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_amount = krw * 0.5
                    upbit.buy_market_order("KRW-STORJ", buy_amount * 0.9995)
        else:
            btc = get_balance("STORJ")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-STORJ", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
