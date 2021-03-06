import os
import numpy as np
import pandas as pd
import asyncio

import sys


    

import hvplot.streamz
from streamz import Stream
from streamz.dataframe import DataFrame
import panel as pn

pn.extension()


# from bokeh.plotting import figure, output_file, show
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
import plotly.graph_objects as go
from bokeh.themes.theme import Theme
import holoviews as hv

#Local module
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../Twitter')

import Toufic.price_predictions as price_model


# from Twitter import config as tw
import sqlite3
import time
import os.path
import os



def initialize():
    """Initialize the dashboard"""
    tweets_stream = Stream()
    columns = ['created_at', 'user_name', 'tweets', 'sentiments', 'polarity']
    data = {"created_at":[],"user_name":[],"tweets":[],"sentiments":[],"polarity":[]}
    tweets_example = pd.DataFrame(
        data=data, columns=columns)
    
    
    tweets_df = DataFrame(tweets_stream, example=tweets_example) 
    
    # Initialize Streaming DataFrame for Signals
    
    price_stream = Stream()
    predictions_example = pd.DataFrame({'Date':[],'actual':[], 'lstm':[], 'regression':[]})

    
#     predictions_example = pd.DataFrame({'MSFT_actual':[], 'MSFT_lstm':[], 'MSFT_regression':[]}, columns=['MSFT_actual','MSFT_lstm','MSFT_regression'], index=pd.DatetimeIndex([]))
                                                                                                                      
    predictions_streamz_df = DataFrame(price_stream, example=predictions_example)

    # Initialize Streaming DataFrame for the signals
    dashboard = build_dashboard(tweets_df, predictions_streamz_df)
    
    return tweets_stream, price_stream, dashboard


def build_dashboard(tweets,predictions_streamz_df):
    """Build the dashboard. changes the css, styles and creates empty place holders for tables, tweets and graphs """
    
    template = """
    {% extends base %}

    <!-- goes in body -->
    {% block postamble %}
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/solar/bootstrap.min.css">
    {% endblock %}

    <!-- goes in body -->
    {% block contents %}
    {{ app_title }}
    <p/>
    <p style="text-align:center;">
    <img src="https://user-images.githubusercontent.com/4336187/87214331-6d9ef280-c2f9-11ea-9c87-231f5c828a4e.png" height='108'>
    </p>
    
    <br>
    <div class="container">
      <div class="row"> 
        <div class="col-sm">
          {{ embed(roots.B) }}
        </div> 
      </div>
    <div class="container">
      <div class="row"> 
        <div class="col-sm">
          {{ embed(roots.C) }}
        </div> 
      </div>
   
      </div>
    </div>
    {% endblock %}
    <div style="background:<%= 
                (function colorfromint(){
                    if(cola > colb ){
                        return("green")}
                    }()) %>; 
                color: black"> 
            <%= value %>
     </div>
    """

    css = '''
    .panel-widget-box {
      background: #f0f0f0;
      border-radius: 5px;
      border: 1px black solid;
    }

     '''


    theme = Theme(
        json={
        'attrs' : {
            'Figure' : {
                'background_fill_color': 'black',
                'border_fill_color': 'black',
                'outline_line_color': '#444444',
            },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .3,
            },

            'Axis': {
                'major_label_text_color': 'white',
                'axis_label_text_color': 'white',
                'major_tick_line_color': 'white',
                'minor_tick_line_color': 'white',
                'axis_line_color': "white"
            }
        }
    })

    hv.renderer('bokeh').theme = theme

    dashboard = pn.Template(template)

    tweets_table = pn.Column(
        "##### Live Tweet Sentiments:",
        tweets.hvplot.table(
            columns = ['created_at', 'user_name', 'tweets', 'sentiments', 'polarity'], 
            backlog=10,
        ).opts(bgcolor='blue',height=272),
    css_classes=['panel-widget-box'])

    

    
    
    price = pn.Column(
        "##### Pricing Model",
        predictions_streamz_df.hvplot.line(width=1400, grid=True, backlog=500,title="prices").opts( bgcolor='black', legend_position='right'))
    
 
   
    positive_cloud = pn.Column(
    "##### Postive Word Cloud:", pn.pane.PNG('Images/postive_sentiments.png', height=272))
        
    negative_cloud = pn.Column(
    "##### Negative Word Cloud:", pn.pane.PNG('Images/negative_sentiments.png', height=272))
    
    
    clouds = pn.Row(
        positive_cloud,negative_cloud
    )
    
    sentiments = pn.Row(
        tweets_table, clouds
    )
    
    
#     dashboard.add_panel('B',tweets_table)
    dashboard.add_panel('B',sentiments)
    dashboard.add_panel('C',price)

    
    return dashboard


    
def price_data():
    global i
    price_df = price_model.combined_predictions()
    print(f'{price_df}')
    small_df = price_df.rename(columns={'MSFT_actual': 'actual', 'MSFT_lstm': 'lstm','MSFT_regression':'regression' })
    
    print(f'{price_df}')

    return small_df

def twitter_data():
    global counter
    try:
        global db
        with db:
            cur = db.cursor()
            df = pd.read_sql(f"select * from tweets limit 1 offset {counter}", db)
              
    except sqlite3.OperationalError:
        print("Database is locked")
        #wait for 5 seconds and commit
        sleep(5)
    except sqlite3.Error as sqle:
        #wait for 5 seconds and commit
        time.sleep(5)    
        logger.error("Unable to add a new record for some reason: %s" %sqle)
    except Exception as e:
        logger.error("Unable to add a new record: %s" %e)
                
    print(df['tweets'])
        
    return df

    
tweets_stream, price_stream, dashboard = initialize()
dashboard.servable()

db_name = "twitter_sentiments.db"
db_name = os.path.abspath('../Twitter/twitter_sentiments.db')
print(db_name)
db = sqlite3.connect(db_name, timeout=10)
i=0
from streamz.dataframe import Random
async def main():
   
    global i
    global tweets_stream
    global price_stream
    global counter
    loop = asyncio.get_event_loop() 
    
    price_df = price_data()
    price_stream.emit(price_df)
    while (True):

        #twitter feed
        tweets_df = twitter_data()
        if (tweets_df.empty):
            pass
        else:
            tweets_stream.emit(tweets_df)
            counter += 1 
            print(f"tweets {tweets_df}")
            
            
            
        await asyncio.sleep(1)
    
counter = 1
loop = asyncio.get_event_loop()
try:    
    loop.run_until_complete(main())  
#     asyncio.run(main())

except KeyboardInterrupt:
    print("Application force stopped by the trader.")
except Exception as ex:
    print(f"An Exception Occured, please investigate: {ex}")
except SystemExit as sye:
    print(f"System Exited for some reason {sye}")
finally:
    
    pass
     

    
    