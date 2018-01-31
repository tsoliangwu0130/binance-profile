from binance.client import Client
from config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    client = Client(app.config['API_KEY'], app.config['API_SECRET'])
    balance = client.get_asset_balance(asset='BTC')
    print(balance)
    return 'Hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
