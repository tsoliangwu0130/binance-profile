import datetime
import json
from binance.client import Client, BinanceAPIException
from config import Config
from flask import render_template, Flask

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
    account['orders'] = orders

    return account


@app.route('/')
def index():
    account = get_account()

    return render_template('index.html', account=account)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
