import pandas as pd
import time, sys, asyncio

from streamz import Stream
from streamz.dataframe import DataFrame

import os
basepath = os.path.abspath(os.path.dirname(__file__)) + "/"

def combined_predictions():
    combined_df = pd.read_csv(basepath + 'price_data.csv')
    return combined_df

stream = Stream()
predictions_stream = pd.DataFrame({'MSFT_actual':[], 'MSFT_lstm':[], 'MSFT_regression':[]})

predictions_streamz_df = DataFrame(stream, example=predictions_stream)
