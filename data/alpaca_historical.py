import alpaca_trade_api as tradeapi
import config
from datetime import datetime, timedelta, date

# initiate trading api for orders, etc.
api = tradeapi.REST(
    config.API_KEY,
    config.SECRET_KEY,
    api_version='v2'
    )

timeframe = '1D' #1Min, 5Min, 15Min, 1D
tickers = ['MSFT', 'AAPL', 'BRK.B']
limit = '1000' #between 1 and 1000. default is 100.
end_date = date.today()
start_date = end_date - timedelta(365)

stocks_history = api.get_barset(
    symbols=tickers,
    timeframe=timeframe,
    limit=limit,
    start=start_date,
    end=end_date,
    after=None,
    until=None
).df
