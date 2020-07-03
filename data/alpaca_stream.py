import alpaca_trade_api as tradeapi
import websocket, json, config

def on_open(ws):
    print('opened')
    auth_data = {
        'action': 'authenticate',
        'data': {
            'key_id': config.API_KEY,
            'secret_key': config.SECRET_KEY
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
    config.ALPACA_WS_URL,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close
    )

ws.run_forever()