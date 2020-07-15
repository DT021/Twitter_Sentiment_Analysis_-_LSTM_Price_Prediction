#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_api
import json
import time
import sqlite3
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import regex as re
import nltk
nltk.download('stopwords')
# NLTK list of stopwords
from nltk.corpus import reuters, stopwords
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import pickle
from wordcloud import WordCloud
import sys 

db = sqlite3.connect("twitter_sentiments.db", timeout=15)
cur = db.cursor()
data = ""

FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger()



class TweetListener(tweepy.StreamListener):
    
    global db
    global cur
    global loaded_model
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.num_tweets =0
        super(TweetListener, self).__init__()

    def on_status(self, tweet):

        if hasattr(tweet, "retweeted_status"): #Check if Retweet
            pass
        else:
            if hasattr(tweet,"extended_tweet"):
                full_tweet = tweet.extended_tweet["full_text"]
            else:
                full_tweet = tweet.text
            data = {"handle":f"{tweet.user.screen_name}", "name":f"{tweet.user.name}", "tweet":f"{full_tweet}"}
            print(data)
            print(full_tweet)
            polarity, sentiments = rnn_lstm_sentiment(tweet.text)
            print(f" polarity {polarity}, prediction {sentiments}")
            try:
                with db:
                    cur.execute("INSERT INTO tweets(created_at,user_name,tweets,sentiments,polarity) values(?,?,?,?,?)", (tweet.created_at,
                                                                tweet.user.name,full_tweet,sentiments,polarity))
                    db.commit()
                    
            except sqlite3.OperationalError:
                print("Database is locked")
                counter-=1
                #wait for 5 seconds and commit
                sleep(5)
            except sqlite3.Error as sqle:
                #wait for 5 seconds and commit
                time.sleep(5)    
                logger.error("Unable to add a new record for some reason: %s" %sqle)
            except Exception as e:
                logger.error("Unable to add a new record: %s" %e)
     
            try:
                self.num_tweets +=1
                if self.num_tweets <= 2:                    
                    return True
                else:
                    return False
            except AttributeError:
                logger.error(tweet.text)

    def on_error(self, status):
        logger.error(status)
        return False



def initialize():
    """ load the rnn lstm model """
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("best_model.hdf5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=[
            "accuracy",
        ],
    )
    return loaded_model

def clean_text(text):
    """
        text: a string        
        return: modified initial string
    """
    
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    REMOVE_STOCK_SYMBOLS = re.compile('(\$\w+)(\w*[a-zA-Z]\w*)')
    REMOVE_AT_THE_RATE_SYMBOLS = re.compile('(\@\w+)(\w*[a-zA-Z]\w*)')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    stopwords = nltk.corpus.stopwords.words('english')
    #Stopwords
    list_of_stopwords = ['rt', 'zacks','imperial capital brokers','brokers','valuengine','inc','price traget','article','join','investment research',
                        'zacks investment research']
    stopword_from_nltk = set(stopwords)
    STOPWORDS = stopword_from_nltk.union(list_of_stopwords)
    
    text = text.lower() # lowercase text
    text = re.sub("(?P<url>https?://[^\s]+)", "", text) #remove url
    text = REMOVE_AT_THE_RATE_SYMBOLS.sub('',text)                
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = REMOVE_STOCK_SYMBOLS.sub('',text) # remove stock symbols
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
    text = text.replace('x', '')
#    text = re.sub(r'\W+', '', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    
    return text

def rnn_lstm_sentiment(tweets):
    """ for all tweets look at the sentiment analysis"""
    
    # cleaning up the tweets and adding more stopwords
  
    tweets = clean_text(tweets)
    print(f'inside lstm: {tweets}')
    # loading Tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    tw = tokenizer.texts_to_sequences([tweets])
    print(tw)
    tw = pad_sequences(tw,maxlen=10)
    prediction = int(loaded_model.predict(tw).round().item())
    polarity = loaded_model.predict(tw)[0][0]
    print(f'inside lstm {prediction} {type(polarity)}')
    
    return float(polarity), prediction
    

def database_table():
    """ create a database table """
    global db
    global cur    
    with db:
        cur.execute('''create table if not exists tweets (created_at DATETIME, user_name VARCHAR, tweets VARCHAR, sentiments INT, polarity FLOAT)''')
        db.commit()

loaded_model = initialize()        
database_table()       
def main(keywords):
    api = create_api()
    
    try:
        logger.info("listening for new tweets...")
        tweets_listener = TweetListener(api)
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=keywords, languages=["en"])
        print(f'----{data}')
    except KeyboardInterrupt:
        logger.info("Stopped")
        db.close()
        sys.exit("Server stopped by the trader")
    finally:
        logger.info('Done.')
        stream.disconnect()
        
        

        
# if __name__ == "__main__":
    
# #     search_words = ["AAPL", "$AAPL"]
#     input_words = input("Please enter a ticker: ")
#     input_words=input_words.upper()
#     search_words = []
#     search_words.append(input_words)
#     search_words.append('$'+input_words)
#     logger.info(f'search words are: {search_words}')
#     main(search_words)
    
    

