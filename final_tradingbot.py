import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
import praw  

# Sentiment Analysis Function (TextBlob)
def get_sentiment_from_text(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns sentiment polarity

# Real Reddit Sentiment Analysis Function
def get_reddit_sentiment(keyword="EURUSD"):
    # Connect to Reddit API
    reddit = praw.Reddit(
        client_id="ctafNvTUO0f1QI6cPvWYcg",     
        client_secret= "TwkFSM-NcBnK5sL96dW1ZY6wLwuqog", 
        user_agent="Murky-Lawfulness-330"       
    )

    subreddit = reddit.subreddit("Forex")  
    
    # Search for recent posts containing the keyword
    posts = subreddit.search(keyword, sort="new", limit=10)  

    sentiment_scores = []

    for post in posts:
        text = post.title + " " + (post.selftext or "")
        sentiment = get_sentiment_from_text(text)
        sentiment_scores.append(sentiment)

    if sentiment_scores:
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    else:
        average_sentiment = 0  

    print(f"Average Reddit Sentiment for {keyword}: {average_sentiment}")
    return average_sentiment

# Price Momentum Calculation
def calculate_momentum(price_data, window=30):
    price_data['Momentum'] = price_data['Close'].rolling(window=window).mean()
    price_data.dropna(inplace=True)
    return price_data

# Machine Learning Model for Price Prediction
def create_ml_model(price_data):
    # Extract features (momentum and sentiment) and labels (price up/down)
    price_data['Sentiment'] = price_data['Sentiment'].shift(-1)
    price_data['Price_Change'] = price_data['Close'].pct_change().shift(-1)
    
    price_data['Label'] = (price_data['Price_Change'] > 0).astype(int)
    
    features = ['Momentum', 'Sentiment']
    price_data.dropna(inplace=True)
    
    X = price_data[features]
    y = price_data['Label']
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=500, max_depth=5, min_samples_split=10)
    model.fit(X_train, y_train)
    
    # Test the model
    y_pred = model.predict(X_test)
    print(f'Model Accuracy: {accuracy_score(y_test, y_pred)}')
    
    return model

# Backtesting Framework
def backtest_strategy(price_data, model):
    price_data['Prediction'] = model.predict(price_data[['Momentum', 'Sentiment']])
    price_data['Signal'] = price_data['Prediction'].shift(1)
    price_data.dropna(inplace=True)

    price_data['Returns'] = price_data['Signal'] * price_data['Price_Change']
    price_data['Cumulative_Returns'] = (1 + price_data['Returns']).cumprod()

    print(price_data[['Cumulative_Returns']].tail())
    
    # Plot the backtest results
    plt.figure(figsize=(10, 6))
    plt.plot(price_data['Cumulative_Returns'], label='Cumulative Strategy Returns')
    plt.plot(price_data['Cumulative_Returns'].iloc[0] * (1 + price_data['Price_Change']).cumprod(), label='Buy and Hold', linestyle='--')
    plt.legend()
    plt.title('Backtest of Sentiment + Momentum Strategy')
    plt.show()

# Real-Time Alert System for Price and Sentiment
def real_time_alert(price_data, sentiment_score, threshold=0.5):
    # Check for price jump and high sentiment polarity
    if sentiment_score > threshold:
        print(f"High sentiment detected: {sentiment_score}")
        if price_data['Price_Change'].iloc[-1] > 0.02: 
            print("Price Jump Detected! Consider Going Long.")
        elif price_data['Price_Change'].iloc[-1] < -0.02:
            print("Price Drop Detected! Consider Going Short.")
    else:
        print("Sentiment is neutral.")

# Main function to run the trading bot
def run_trading_bot():
    # Fetch Data from Yahoo Finance (EUR/USD data)
    print("Fetching data for EURUSD...")
    data = yf.download("EURUSD=X", interval="5m", period="7d") 
    
    # Add Momentum calculation
    data = calculate_momentum(data)
    
    # Simulate sentiment data
    print("Fetching Reddit sentiment...")
    live_sentiment = get_reddit_sentiment()  
    
    # Assign same sentiment across data for now (simple integration)
    data['Sentiment'] = live_sentiment

    # Train ML Model
    print("Training Machine Learning model...")
    model = create_ml_model(data)
    
    # Backtest Strategy
    print("Backtesting strategy...")
    backtest_strategy(data, model)
    
    # Real-time Alerts
    print("Monitoring real-time alerts...")
    for i in range(10):  # Simulating real-time updates
        sentiment_score = get_reddit_sentiment()
        real_time_alert(data, sentiment_score)
        time.sleep(60) 

# Run the trading bot
if __name__ == "__main__":
    run_trading_bot()
