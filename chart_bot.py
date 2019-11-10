from dotenv import load_dotenv
from datetime import datetime
import requests
import os
import chart_db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TARGET = os.environ.get("TARGET")
BASE = os.environ.get("BASE")
DBFILE = os.environ.get("DBFILE")


def get_market_price_unnamed_exchange(target, base, time):
    unnamed_api_url = "https://api.unnamed.exchange/v1/Public/Chart?market={}_{}&minutes=5".format(
        target, base, str(time - 300) + "000")
    response_target = requests.get(unnamed_api_url).json()[0]

    for_insert = (f"{response_target['openTime']}"[:-3],
                  f"{response_target['closeTime']}"[:-3],
                  f"{response_target['open']:.8f}",
                  f"{response_target['high']:.8f}",
                  f"{response_target['low']:.8f}",
                  f"{response_target['close']:.8f}",
                  f"{response_target['volume']}",
                  f"{response_target['baseVolume']}")

    open = response_target['open']
    high = response_target['high']
    low = response_target['low']
    close = response_target['close']
    # base通貨のBTC価格を取得
    unnamed_api_url = "https://api.unnamed.exchange/v1/Public/Ticker?market={}_{}".format(
        base, "BTC")
    response_base = requests.get(unnamed_api_url).json()
    btc = response_base['close']
    open_jpy, high_jpy, low_jpy, close_jpy = get_market_price_doge2jpy(open, high, low, close, btc)
    open_usd, high_usd, low_usd, close_usd = get_market_price_doge2usd(open, high, low, close, btc)

    for_insert = for_insert + (f"{open_jpy:.10f}", f"{high_jpy:.10f}", f"{low_jpy:.10f}", f"{close_jpy:.10f}",
                               f"{open_usd:.10f}", f"{high_usd:.10f}", f"{low_usd:.10f}", f"{close_usd:.10f}")

    return for_insert


def get_market_price_doge2jpy(open, high, low, close, btc):
    # coinecheckのAPIを指定
    coincheck_btc_jpy_api_url = "https://coincheck.com/api/ticker"
    coincheck_btc_jpy_api_response = requests.get(
        coincheck_btc_jpy_api_url).json()
    btc_jpy = coincheck_btc_jpy_api_response['last']
    # zaifのAPIを指定
    # zaif_btc_jpy_api_url = "https://api.zaif.jp/api/1/last_price/btc_jpy"
    # zaif_btc_jpy_api_response = requests.get(zaif_btc_jpy_api_url).json()
    # btc_jpy = zaif_btc_jpy_api_response['last_price']
    # 日本円を計算
    open_jpy = open * btc * btc_jpy
    high_jpy = high * btc * btc_jpy
    low_jpy = low * btc * btc_jpy
    close_jpy = close * btc * btc_jpy
    return round(open_jpy, 10), round(high_jpy, 10), round(low_jpy, 10), round(close_jpy, 10)


def get_market_price_doge2usd(open, high, low, close, btc):
    # blockchainのAPIを指定
    blockchain_btc_usd_api_url = "https://blockchain.info/ticker"
    blockchain_btc_usd_api_response = requests.get(
        blockchain_btc_usd_api_url).json()
    btc_usd = blockchain_btc_usd_api_response['USD']['last']
    # アメリカドルを計算
    open_usd = open * btc * btc_usd
    high_usd = high * btc * btc_usd
    low_usd = low * btc * btc_usd
    close_usd = close * btc * btc_usd
    return round(open_usd, 10), round(high_usd, 10), round(low_usd, 10), round(close_usd, 10)


if __name__ == '__main__':
    print('start')
    now = datetime.now()
    insert_value = get_market_price_unnamed_exchange(TARGET, BASE, int(now.timestamp()))
    print(insert_value)
    chart_db.chart_db_insert(DBFILE, insert_value)
    print('end')
