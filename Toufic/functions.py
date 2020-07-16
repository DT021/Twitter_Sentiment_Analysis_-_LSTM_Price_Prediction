import pandas as pd
import numpy as np
import sys
sys.path.append('../')
import data.config as config
import requests, time
from pathlib import Path

def get_stock_closing_prices(symbols, output_size='full', name='stocks_history', api_key=config.ALPHA_VANTAGE_API): #symbol must be a list
    """
    function=TIME_SERIES_INTRADAY
    interval (required): 1min, 5min, 15min, 30min, 60min
    outputsize (required): compact = last 100 data points, full = all data
    
    function=TIME_SERIES_DAILY
    outputsize (optional): compact = last 100 data points, full = all data
    """
    # constants
    BASE_URL = 'https://www.alphavantage.co/query?function='
    
    df = pd.DataFrame()
    symbols = symbols
    output_size = output_size
    interval = kwargs.get('interval', None)
    for symbol in symbols:
        # set request URL for GET request
        if interval == None:
            request_URL = BASE_URL + \
f'{function}&symbol={symbols}&outputsize={output_size}&apikey={api_key}'
        else:
            request_URL = BASE_URL + \
f'{function}&symbol={symbols}&interval={interval}&outputsize={output_size}&apikey={api_key}'
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
    if y.all() != None:
        scaler.fit(y)
        y = scaler.transform(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X, y, scaler
    
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, scaler

def predict_prices(
    df,
    window,
    feature_col_number,
    target_col_number,
    model_path,
    predictions_path
):
    
    from tensorflow.keras.models import model_from_json, load_model
    
    # chunk data with a rolling window
    X, y = window_data(
        df=df,
        window=window,
        feature_col_number=feature_col_number,
        target_col_number=target_col_number
    )
    
    # scale data
    X, y, scaler = scale_and_reshape_data(X=X, y=y)
    
    # load model
    model = load_model(model_path)

    # predict prices
    predicted = model.predict(X)

    # Recover the original prices instead of the scaled version
    predicted_prices = scaler.inverse_transform(predicted)
    real_prices = scaler.inverse_transform(y.reshape(-1, 1))

    predictions = pd.DataFrame(
        index=df[window+1:].index,
        data = {
            "Real": real_prices.ravel(),
            "Predicted": predicted_prices.ravel()
        }
    )

    predictions.to_csv(Path(predictions_path))
    
    return predictions