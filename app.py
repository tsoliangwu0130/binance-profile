import datetime
import json
from binance.client import Client, BinanceAPIException
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
client = Client(app.config['API_KEY'], app.config['API_SECRET'])
symbols = client.get_exchange_info()['symbols']


def get_account():
    account = client.get_account()
    balances = [b for b in account['balances'] if (float(b['free']) + float(b['locked']) > 0)]
    account['balances'] = balances

    orders = []
    for symbol in symbols:
        if any(symbol['symbol'].startswith(balance['asset']) for balance in balances):
            try:
                order = client.get_all_orders(symbol=symbol['symbol'])
                orders.append(order) if order else None
            except BinanceAPIException:
                continue

    for order in orders:
        for o in order:
            date = datetime.datetime.fromtimestamp(int(o['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            o['date'] = date

    account['orders'] = orders
    print(json.dumps(orders, indent=4, sort_keys=''))
    return account


@app.route('/')
def index():
    account = get_account()
    # print(json.dumps(account, indent=4))

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
