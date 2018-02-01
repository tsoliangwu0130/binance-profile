import json
from binance.client import Client
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
client = Client(app.config['API_KEY'], app.config['API_SECRET'])


def get_symbols(symbol):
    usdt_symbols = ['BTC', 'ETH', 'NEO', 'BNB', 'LTC', 'BCC']
    hold_symbols = ['BTC', 'ETH']
    symbols = []

    for hold in hold_symbols:
        if symbol == hold:
            continue
        else:
            symbols.append(symbol + hold)

    if symbol in usdt_symbols:
        symbols.append(symbol + 'USDT')

    return symbols


def get_blances():
    info = client.get_account()
    balances = []

    for balance in info['balances']:
        total_balance = float(balance['free']) + float(balance['locked'])
        if total_balance > 0:
            tickers = []
            for symbol in get_symbols(balance['asset']):
                try:
                    ticker = client.get_symbol_ticker(symbol=symbol)
                    tickers.append(ticker)
                except:
                    continue

            balances.append({
                'assest': balance['asset'],
                'tickers': tickers,
                'free': balance['free'],
                'locked': balance['locked']
            })

    return balances


def get_all_orders():
    orders = client.get_all_orders(symbol='ICXBTC')
    print(json.dumps(orders, indent=4, sort_keys=True))


@app.route('/')
def index():
    balances = get_blances()
    print(balances)
    # get_all_orders()

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
