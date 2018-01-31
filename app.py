from binance.client import Client
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    client = Client(app.config['API_KEY'], app.config['API_SECRET'])
    info = client.get_account()

    for balance in info['balances']:
        total_balance = float(balance['free']) + float(balance['locked'])
        if total_balance > 0:
            print('{}: {}'.format(balance['asset'], total_balance))

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
