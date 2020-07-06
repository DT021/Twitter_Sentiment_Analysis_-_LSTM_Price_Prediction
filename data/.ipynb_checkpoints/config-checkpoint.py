import os

# constants
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
# API_BASE_URL = 'https://paper-api.alpaca.markets/'
API_DATA_URL = 'https://data.alpaca.markets'
ALPACA_WS_URL = 'wss://data.alpaca.markets/stream'
# POLYGON_WS_URL = 'wss://alpaca.socket.polygon.io/stocks	'

HEADERS = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY,
}