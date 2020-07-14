import pandas as pd
import numpy as np
import sys
sys.path.append('../')
import data.config as config
import requests, time
from pathlib import Path

def get_stock_closing_prices(symbols, output_size='full', name='stocks_history', api_key=config.ALPHA_VANTAGE_API): #symbol must be a list
    # constants
    BASE_URL = 'https://www.alphavantage.co/query?function='
    FUNCTION = 'TIME_SERIES_DAILY' #returns daily data vs. intraday data
    
    # create dataframe for data
    df = pd.DataFrame()
    # set parameters
    symbols = symbols
    output_size = output_size
    
    # loop through tickers and sent GET request to API
    for symbol in symbols:
        # set request URL for GET request
        request_URL = BASE_URL + \
f'{FUNCTION}&symbol={symbol}&outputsize={output_size}&apikey={api_key}'
        # send GET request
        r = requests.get(request_URL)
        # create dataframe from GET response (transpose dataframe, as response flips
        # rows and columns (dates are in columns instead of rows)
        _ = pd.DataFrame(r.json()['Time Series (Daily)']).transpose()
        # rename columns to include ticker
        columns = [
            f'{symbol}_open',
            f'{symbol}_high',
            f'{symbol}_low',
            f'{symbol}_close',
            f'{symbol}_volume'
        ]
        _.columns = columns
        # join dataframe to "master" dataframe
        df = df.join(_, how='outer')
        time.sleep(15) #sleeping due to call limit on api (5 calls per minute)
        # sort index in ascending order
        df.sort_index(ascending=True, inplace=True)
        df.to_csv(f'{name}.csv')
    return df

def window_data(df, window, feature_col_number, target_col_number):
    """
    This function accepts the column number for the features (X) and the target (y).
    It chunks the data up with a rolling window of Xt - window to predict Xt.
    It returns two numpy arrays of X and y.
    """
    X = []
    y = []
    for i in range(len(df) - window - 1):
        features = df.iloc[i : (i + window), feature_col_number]
        target = df.iloc[(i + window), target_col_number]
        X.append(features)
        y.append(target)
    return np.array(X), np.array(y).reshape(-1, 1)

def train_test_split(X,y,split_pct=0.7):
    
    # Use percent (70% by default) of the data for training and the remainder for testing
    split = int(split_pct * len(X))
    X_train = X[: split - 1]
    X_test = X[split:]
    y_train = y[: split - 1]
    y_test = y[split:]
    
    return X_train, X_test, y_train, y_test

def one_lstm(df, feature_column, target_column, window_size, batch_size, dropout_fraction,\
             epoch, name='exported_1lstm_model', *args, **kwargs):
    
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    
    from sklearn.preprocessing import MinMaxScaler
    
    split_pct = kwargs.get('split_pct',0.7)
    check_point = kwargs.get('check_point',None)
    early_stop = kwargs.get('early_stop', None)
    
    X, y = window_data(df, window_size, feature_column, target_column)

    X_train, X_test, y_train, y_test = train_test_split(X,y,split_pct)

    # Use the MinMaxScaler to scale data between 0 and 1.
    scaler = MinMaxScaler()
    scaler.fit(X)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    scaler.fit(y)
    y_train = scaler.transform(y_train)
    y_test = scaler.transform(y_test)

    # Reshape the features for the model
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # Define the LSTM RNN model.
    model = Sequential()
    # Layer 1
    model.add(LSTM(
        units=window_size,
        input_shape=(X_train.shape[1], 1))
        )
    model.add(Dropout(dropout_fraction))
    # Output layer
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    if check_point != None and early_stop != None:
        model.fit(
            X_train,
            y_train,
            epochs=epoch,
            shuffle=False,
            batch_size=batch_size,
            verbose=0,
            callbacks = [check_point, early_stop]
        )
    else:
        model.fit(
            X_train,
            y_train,
            epochs=epoch,
            shuffle=False,
            batch_size=batch_size,
            verbose=0
        )
        model.save(f'{name}.h5')

    # Evaluate the model
    loss = model.evaluate(X_test, y_test, verbose=0)

    # Make some predictions
    predicted = model.predict(X_test)

    # Recover the original prices instead of the scaled version
    predicted_prices = scaler.inverse_transform(predicted)
    real_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Create a DataFrame of Real and Predicted values
    stocks = pd.DataFrame({
        "Real": real_prices.ravel(),
        "Predicted": predicted_prices.ravel()
    })
    
#     model_json = model.to_json()
#     with open(f'{name}.json', 'w') as json_file:
#         json_file.write(model_json)
#     model.save_weights(f'{name}.h5')
    
    return model, loss, stocks

def two_lstm(df, feature_column, target_column, window_size, batch_size, dropout_fraction,\
             epoch, split_pct, name='exported_2lstm_model', *args, **kwargs):
    
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    
    from sklearn.preprocessing import MinMaxScaler
    
    split_pct = kwargs.get('split_pct',0.7)
    check_point = kwargs.get('check_point',None)
    early_stop = kwargs.get('early_stop', None)
    
    X, y = window_data(df, window_size, feature_column, target_column)

    X_train, X_test, y_train, y_test = train_test_split(X,y,split_pct)

    # Use the MinMaxScaler to scale data between 0 and 1.
    scaler = MinMaxScaler()
    scaler.fit(X)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    scaler.fit(y)
    y_train = scaler.transform(y_train)
    y_test = scaler.transform(y_test)

    # Reshape the features for the model
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    # Define the LSTM RNN model.
    model = Sequential()
    # Layer 1
    model.add(LSTM(
        units=window_size,
        return_sequences=True,
        input_shape=(X_train.shape[1], 1))
        )
    model.add(Dropout(dropout_fraction))
    # Layer 2
    model.add(LSTM(units=row['window size']))
    model.add(Dropout(dropout_fraction))
    # Output layer
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    if check_point != None and early_stop != None:
        model.fit(
            X_train,
            y_train,
            epochs=epoch,
            shuffle=False,
            batch_size=batch_size,
            verbose=0,
            callbacks = [check_point, early_stop]
        )
    else:
        model.fit(
            X_train,
            y_train,
            epochs=epoch,
            shuffle=False,
            batch_size=batch_size,
            verbose=0
        )
        model.save(f'{name}.h5')

    # Evaluate the model
    loss = model.evaluate(X_test, y_test, verbose=0)

    # Make some predictions
    predicted = model.predict(X_test)

    # Recover the original prices instead of the scaled version
    predicted_prices = scaler.inverse_transform(predicted)
    real_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Create a DataFrame of Real and Predicted values
    stocks = pd.DataFrame({
        "Real": real_prices.ravel(),
        "Predicted": predicted_prices.ravel()
    })
    
#     model_json = model.to_json()
#     with open(f'{name}.json', 'w') as json_file:
#         json_file.write(model_json)
#     model.save_weights(f'{name}.h5')
    
    return model, loss, stocks

def scale_and_reshape_data(X, y=None):
    
    from sklearn.preprocessing import MinMaxScaler
    
    scaler = MinMaxScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    if y != None:
        scaler.fit(y)
        y = scaler.transform(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X, y
    
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X