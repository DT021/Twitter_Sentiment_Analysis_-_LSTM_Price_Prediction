import os

# constants
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
API_DATA_URL = 'https://data.alpaca.markets'
ALPACA_WS_URL = 'wss://data.alpaca.markets/stream'

ALPHA_VANTAGE_API = os.getenv('ALPHA_VANTAGE_API_KEY')

HEADERS = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY,
}