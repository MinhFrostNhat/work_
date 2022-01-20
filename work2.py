import requests
from work import set_log
import sqlite3
import time
import numpy as np


np.test

logger = set_log()


def run():
    try:
        endpoint = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        body = {
                "page": 1,
                "rows": 20,
                "payTypes": [],
                "asset": "USDT",
                "tradeType": "BUY",
                "fiat": "VND",
                # "publisherType":null,
                "merchantCheck": False,
            }
        headers = {
                "Content-Type": "application/json",
            }
        logger.info("status 200: ok")
    except Exception as e:
        return f"logger.error('error')"
    try:
            response = requests.post(url=endpoint, json=body, headers=headers)
            content = response.json()['data']
            with sqlite3.connect('price.db') as conn:
                curs = conn.cursor()
                curs.execute("CREATE TABLE IF NOT EXISTS price (Price REAL)")
                logger.info('CREATE TABLE')
                for each in content:
                    price = float(each['adv']['price'])
                    print(price)
                    curs.execute("INSERT INTO price VALUES (?)", (price,))
                    logger.info('INSERT DATA TO DATABASE')
    except Exception as E:
            return f"{logger.error('error json shutdown')}"
    try:
                conn = sqlite3.connect('price.db')
                cur = conn.cursor()
                cur.execute("SELECT AVG(price) FROM price")
                rows = cur.fetchall()
                for row in rows:
                    logger.warning(row)
    except Exception as e:
        return logger.error('???')
if __name__== "__main__" :
    start_time = time.time()
    seconds = 0
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            seconds = seconds + 60
            run()
