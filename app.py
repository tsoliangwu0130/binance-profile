import datetime
import json
from binance.client import Client, BinanceAPIException
from coinmarketcap import Market
from config import Config
from flask import render_template, Flask

app = Flask(__name__)
app.config.from_object(Config)
client = Client(app.config['API_KEY'], app.config['API_SECRET'])
symbols = client.get_exchange_info()['symbols']
coinmarketcap = Market()

symbol_to_id = {
    'BTC': 'bitcoin',
    'BNB': 'binance-coin',
    'ETH': 'ethereum',
    'KNC': 'kyber-network',
    'ICX': 'icon',
    'TNB': 'time-new-bank',
    'USDT': 'tether'
}


def get_account():
    account = client.get_account()

    balances = []
    for balance in account['balances']:
        total = float(balance['free']) + float(balance['locked'])
        if total > 0:
            balance['total'] = total
            asset_id = symbol_to_id[balance['asset']]
            balance['price_usd'] = total * float(coinmarketcap.ticker(asset_id)[0]['price_usd'])
            balances.append(balance)
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

    print(json.dumps(account, indent=4))

    return account


@app.route('/')
def index():
    account = get_account()

    return render_template('index.html', account=account)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
