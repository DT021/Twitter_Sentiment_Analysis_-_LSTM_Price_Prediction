# FINTECH-Project-02 (Team 9)

## Members
- Shubhra Bhatnagar
- Steffen Westerburger
- Toufic Lawand

## Project scope
An ML-backed robo advisory platform that provides insights on when to buy and/or sell a particular stock in order to maximize profits. 

### What marks a success
A functioning algo trading model based on one of the deep learning models and/or NLP with static vizualizations.

### Technologies used
- AWS Cloud/Azure
	- Sagemaker
- Twitter API
- Alpaca (or some other broker) API
- Google Colab/Azure

### Tickers to use for analysis and model building
- AAPL
- BRK.B

## Outline

### Build, train and test models
Build the models for twitter sentiment analysis (using RNN LSTM), as well as price prediction (using regression and deep learning). After training the models, generate signals to buy/sell/hold the stock 

**Models used for sentiment analysis:**
- recurrent neural networks (RNN LSTM) 
- Vader

**Models to be used for price prediction:**
- long short term network (LSTM)
- regression analysis

### Compare models and choose which one
Use confusion and classification matrixes to show the performance of the models and choose which ones to 

### Static graphs
Create (static) graphs that show model results

_OPTIONAL_
**Signal generation:**
- moving average
- taking predicted price as a trigger for the signal (compared to the current market price)
- Support Vector Machines (gets features from price prediction models, current price and moving average)

_OPTIONAL_
### Vizualization
Create graphs to display prices and signals, as well as a twitter feed with the general sentiment for the stock.


