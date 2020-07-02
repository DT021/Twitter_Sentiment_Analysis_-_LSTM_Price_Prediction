import alpaca_trade_api as tradeapi
import os, websocket, json

# constants
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
# ALPACA_API_BASE_URL = 'https://paper-api.alpaca.markets/'
# ALPACA_API_DATA_URL = 'https://data.alpaca.markets'
ALPACA_WS_URL = 'wss://data.alpaca.markets/stream'
# POLYGON_WS_URL = 'wss://alpaca.socket.polygon.io/stocks	'

api = tradeapi.REST(
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    api_version='v2'
    )

# connection = StreamConn()

# @connection.on(r'trade_updates$')
# async def on_

def on_open(ws):
    print('opened')
    auth_data = {
        'action': 'authenticate',
        'data': {
            'key_id': ALPACA_API_KEY,
            'secret_key': ALPACA_SECRET_KEY
            }
    }
    ws.send(json.dumps(auth_data))

    listen_message = {
        'action': 'listen',
        'data': {
            'streams': ['AM.AAPL']
        }
    }

    ws.send(json.dumps(listen_message))

def on_message(ws, message):
    print(message)

def on_close(ws):
    print('closed connection')

ws = websocket.WebSocketApp(
    ALPACA_WS_URL,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close
    )

ws.run_forever()