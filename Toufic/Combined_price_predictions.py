import pandas as pd
import numpy as np
import panel as pn
import requests, time, pickle, sys, asyncio
import hvplot.pandas, hvplot.streamz
from streamz import Stream
from streamz.dataframe import DataFrame

from pathlib import Path
from datetime import datetime
from sklearn.metrics import mean_squared_error
sys.path.append(../)
from Toufic.functions import *

%matplotlib inline

MSFT_df = pd.read_csv(
    Path('data/stocks_history.csv'),
    index_col='Unnamed: 0',
    infer_datetime_format=True,
    parse_dates=True
)
dropped_columns = [
    'MSFT_open',
    'MSFT_high',
    'MSFT_low',
    'AMD_close',
    'AMD_open',
    'AMD_high',
    'AMD_low',
    'TSLA_close',
    'TSLA_open',
    'TSLA_high',
    'TSLA_low',
    'JNJ_close',
    'JNJ_open',
    'JNJ_high',
    'JNJ_low',
    'REGN_close',
    'REGN_open',
    'REGN_high',
    'REGN_low',
    'GILD_close',
    'GILD_open',
    'GILD_high',
    'GILD_low'
]
MSFT_df.drop(columns=dropped_columns, inplace=True)
MSFT_df.dropna(inplace=True)
MSFT_df.columns = ['Close']

lstm_model_path = 'Toufic/models/JNJ_close_1lstm_model.h5'
feature_column = 0
target_column = 0
predictions_path = 'Toufic/results/20200715_MSFT_LSTM_results.csv'
window = 50
predictions_df = predict_prices(
    df=MSFT_df,
    window=window,
    target_col_number=target_column,
    feature_col_number=feature_column,
    model_path=lstm_model_path,
    predictions_path=predictions_path
)

predictions_df = predictions_df.loc['2020-01-02':,:]
predictions_df.columns = ['MSFT_actual', 'MSFT_lstm']

MSFT_df['MSFT_return'] = MSFT_df['Close'].pct_change() 
MSFT_df['MSFT_lagged_return'] = MSFT_df['MSFT_return'].shift()

regression_model_path = 'Steffen/pickle_regression_model.pkl'
regression_model = pickle.load(open(regression_model_path, 'rb'))

weeks = MSFT_df.index.to_period("w").unique()

training_window = 50
timeframe = len(weeks) - training_window - 1

all_predictions = pd.DataFrame(columns=["MSFT_regression"])

for i in range(0, timeframe):

    test_week = weeks[training_window + i + 1]
    start_of_test_week  = test_week.start_time.strftime(format="%Y-%m-%d")
    end_of_test_week = test_week.end_time.strftime(format="%Y-%m-%d")
    test = MSFT_df.loc[start_of_test_week:end_of_test_week]
    X_test = test["MSFT_lagged_return"].to_frame()
    predictions = regression_model.predict(X_test)
    predictions = pd.DataFrame(predictions, index=X_test.index, columns=["MSFT_regression"])
    all_predictions = all_predictions.append(predictions)

regression_df = all_predictions.loc['2020-01-02':,:]

cumulative_returns = (1 + regression_df['MSFT_regression']).cumprod() - 1

regression_prices = (cumulative_returns +1) * (MSFT_df.loc['2020-01-02','Close'])

combined_df = pd.merge(predictions_df, regression_prices, how='inner', left_index=True, right_index=True)

stream = Stream()
predictions_stream = pd.DataFrame({'MSFT_actual':[], 'MSFT_lstm':[], 'MSFT_regression':[]})

predictions_streamz_df = DataFrame(stream, example=predictions_stream)

i=0

predictions_streamz_df.hvplot()

while True:
    preds_df = combined_df.iloc[i:i+10]
    predictions_streamz_df.emit(preds_df)
    time.sleep(1)
    i+=10