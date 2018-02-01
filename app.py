import json
from binance.client import Client
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
client = Client(app.config['API_KEY'], app.config['API_SECRET'])


def get_info():
    info = client.get_account()

    for balance in info['balances']:
        total_balance = float(balance['free']) + float(balance['locked'])
        if total_balance > 0:
            print('{}: {}'.format(balance['asset'], total_balance))


def get_all_orders():
    orders = client.get_all_orders(symbol='ICXBTC')
    print(json.dumps(orders, indent=4, sort_keys=True))


@app.route('/')
def index():
    get_info()
    get_all_orders()

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
