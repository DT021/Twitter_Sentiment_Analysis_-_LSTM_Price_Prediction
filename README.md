# FINTECH-Project-02 (Team 9)

## Members
- Shubhra Bhatnagar
- Steffen Westerburger
- Toufic Lawand

## Project scope
### Suggested ideas
- Roboadvisory app to provide sentiment on stock in question
	- Lex roboadvisory app linked to Lambda running NLP model for sentiment analysis
- Trading platform
	- Twitter feed relevant to highlighted stock
	- NLP RNN model to analyze twitter feed and provide sentiment
	- news feed with sentiment to buy/hold/sell
	- (?) analyze to PEP tweets vs market volatility and performance
- Algorithmic trading model using the following, comparing their performance, and plotting graphs showing the buy/sell signals:
	- deep learning (RNN)
	- classification
	-
- analysis to determine buy/sell signals
	- Moving average
		- Bollinger bands
		- SMA50, SMA100, SMA200
		- SMA vs Current price
	- regression analysis
	- deep learning model

#### Use cases of AI in Fintech
- Fraud detection and prevention
    - logistic regression
    - support vector machines
    - neural networks
    - naive bayes
- Stock market prediction
    - neural networks
    - k-nearest neighbors regression
    - decision tree regressor
    - bagging regressor
    - gradient descent regression
- Algorithmic trading
    - recurrent neural networks (RNN)
    - long short term network (LSTM)
    - ensemble algorithms
    - support vector machines
- customer service and recommendation
- Source
	- https://pirimidtech.com/top-6-fintech-use-cases-of-machine-learning/

- digital financial coach/advisor
    - natural language processing (NLP)
- transaction search and visualization
- client risk profile
- Source
	- https://towardsdatascience.com/ten-applications-of-ai-to-fintech-22d626c2fdac

### Chosen idea
An ML-backed robo advisory platform that provides insights on when to buy and/or sell a particular stock in order to maximize profits. 

### What marks a success
A functioning algo trading model based on one of the deep learning models and/or NLP with static vizualizations.

### Technologies used
- AWS Cloud
	- Lex
	- Lambda
	- Sagemaker
- Twitter API
- Alpaca (or some other broker) API
- Google Colab

### Tickers to use for analysis and model building
- AAPL
- BRK.B

## Outline

### Build, train and test models
Build the models for sentiment analysis (using NLP), as well as price prediction (using regression and deep learning). After training the models, generate signals to buy/sell/hold the stock 

**Models used for sentiment analysis:**
- recurrent neural networks (RNN)
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


