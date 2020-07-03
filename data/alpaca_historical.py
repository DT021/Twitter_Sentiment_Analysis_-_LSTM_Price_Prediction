import alpaca_trade_api, config, requests, json
from datetime import datetime, timedelta, date

#initiate trading api for orders, etc.
# api = tradeapi.REST(
#     ALPACA_API_KEY,
#     ALPACA_SECRET_KEY,
#     api_version='v2'
#     )

timeframe = '5Min' #1Min, 5Min, 15Min, 1D
tickers = 'MSFT' #include tickers in same quotes separated by commas
limit = '1000' #between 1 and 1000. default is 100.
end_date = date.today()
end_str = end_date.isoformat() + 'T09:30:00-04:00' #ISO Format, ex: '2019-04-15T09:30:00-04:00'
start_date = end_date - timedelta()
start_str = start_date.isoformat() + 'T09:30:00-04:00' #ISO Format, ex: '2019-04-15T09:30:00-04:00'

bars_url = config.API_DATA_URL + \
    f'/v1/bars/{timeframe}?symbols={tickers}&limit={limit}&\
        start={start_str}&end={end_str}'

r = requests.get(bars_url, headers=config.HEADERS)

print(json.dumps(r.json(), indent=4))