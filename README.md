# Trading & Analysis of Stocks based on Proprietary Deep Neural Network Models

*A Deep Neural Network advisory platform that provides price signals and live proprietary financial Twitter senitments for equity trading by Shubra Bhatnagar, Toufic Lawand and Steffen Westerburger* 

![Picture](https://s3.amazonaws.com/prod-www-blackline-com/blog/wp-content/uploads/2019/01/29163118/A-Conversation-With-BlackLines-Machine-Learning-Experts.jpg)

## **Introduction** 

We developed a Deep Neural Network advisory platform that provides price signals and live proprietary financial Twitter senitments for equity trading.

We also compared it with the standard regression model
This is done two different and complimentary ways:

1) We designed, developed, trained and tested a long short-term memory (LSTM) model and a linear regression model. Those models enable us to make predicitions on future stock prices based on historical data.

2) We designed, developed, trained and tested a long short-term memory (LSTM) model  specifically focused on sentiment analysis of tweets on Twitter. This model is uniquely equipped to determine the sentiment of tweets that are talking about individual stocks and classifies the core message as either 'positive' or 'negative'.

These two approaches are combined in a comprehensive dashboard that gives any investor, from individual to big corporation, a powerful tool to predict developments in the stock market.




## **Technology/Platforms:** 

##### Packages used:


- pandas
- numpy
- sklearn
- nltk
- tensorflow.keras
- regex
- wordcloud
- pickle

##### APIs used

- Alpha Vantage API
- Alpaca API
- Tweepy API

##### Cloud computing service
Trained the model using Microsoft `***Azure Cloud Notebook***`(Refer to the setup guide in the `Docs` Folder.


---

### *Data and challenges we ran into during the exploration and clean up process*

- For the first part of the project we used historical stock data provided to us by the Alpha Vantage API. We randomly selected six different stocks (MSFT, AMD, TSLA, JNJ, REGN, GILD). 

- For Sentiment Analysis we downloaded tweets and handclassified 11830 tweets


### **Model 1: Predicting stock prices using sklearn linear regression**
We created a sklearn linear regression model to have a benchmark to compare the LSTM model performance to. We trained and tested the linear regression model for price prediction, using the same data as our LSTM price prediction model.


### **Model 2: Predicitng stock prices LSTM using Tensorflow/Keras**
To predict the stock prices using machine learning, we decided to use LSTM and iterated over several parameters in order to reduce the guesswork in choosing how to train the model. This led to training and evaluating 720 models as a start (using 10 years of daily stock prices), and then through a process of retraining, evaluation and elimination, we drilled down our decision to one model.

![PricingModelTraining](Images/PricingModelTraining.png)

As you can see from the graph below, the LSTM model tracks the real prices more closely than the regression model does. The respective RMSE scores for the LSTM model and the regression models were 5.274 and 18.883 - further showing the difference in the performance between the two models.

!['LSTM vs Regression'](Images/LSTM_vs_Regression_graph.png)

As a bonus, we also exported the best performing models from each of the stocks we used to train, as well as all the evaluation results from the iterations that were performed for the 1- and 2-layer models. We didn't export the results for the 3-layer models because when we first ran the full iterations for all models (1-, 2-, and 3-layer ones) we had forgotten to export the evaluation results into a csv file, so we redid the iterations for the 1- and 2-layer ones only due to limited time.

### **Model 3: Twitter sentiment analysis LSTM using Tensorflow/Keras/NLTK**
add screenshot of graph and summary of findings/use

![SentimentAnalysis](Images/LSTM-SentimentAnalysis.png)

## ** Discussion of Findings **
Evaluation of Sentiment Analyzer

![Comparison_of_Models](Images/comparison_rnn_vader.png)

# TRADING PLATFORM
---

![Dashboard](Images/Dashboard.png)

## CONCLUSION
---


![Dashboard](Images/Conclusion.png)


















