import requests
from work import set_loggin
import sqlite3
import time

logger = set_loggin()


def api_data():
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
            "Content-Type": "application/jsonz",
        }
        response = requests.post(url=endpoint, json=body, headers=headers)
        if response.status_code == 200:
            logger.info("status code 200: ok")
            content = response.json()['data']
            with sqlite3.connect('price.db') as conn:
                curs = conn.cursor()
                curs.execute("CREATE TABLE IF NOT EXISTS price (Price REAL)")
                logger.info('CREATE TABLE')
                for each in content:
                    price = float(each['adv']['price'])
                    curs.execute("INSERT INTO price VALUES (?)", (price,))
                logger.info('INSERT DATA TO DATABASE')
                cur = conn.cursor()
                cur.execute("SELECT AVG(price) FROM price")
                rows = cur.fetchall()
                for rw in rows:
                    for i in rw:
                        if i > 23600:
                            logger.warning(f"it's go to upper, price now is: {i}")
                        else:
                            logger.info(f"ok price now : {i}")
        else:
            logger.error("status code 400: bad request")
            return api_data()
    except Exception:
        logger.error('An error occurred')


def repeat_time():
    start_time = time.time()
    seconds = 0
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            seconds = seconds + 60
            api_data()


if __name__ == "__main__":
    repeat_time()

