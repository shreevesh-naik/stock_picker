# -*- coding: utf-8 -*-
"""stock_recommandation_system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w93jnjzdH2mazLzOp8kmMxwMRJmtSkfg

Libraries
"""

import pandas as pd
import yfinance as yf
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 
import math

"""Choosing the best model"""

#Dataset
dataset = yf.Ticker("PG")
dataset = dataset.history(start="2020-01-01", end="2023-05-10")

del dataset["Dividends"]
del dataset["Stock Splits"]

dataset.isnull().sum()

X = dataset[['Open', 'High', 'Low', 'Volume']]
y = dataset['Close']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
dataset.head(5)

#Random Forest
from sklearn.ensemble import RandomForestRegressor

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the random forest model on the training set
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# Predict the testing set
predicted = rf_regressor.predict(X_test)

# add predicted column to dataset
dataset['Predicted'] = rf_regressor.predict(X)

# print the evaluation metrics
print('Mean Absolute Error:' , metrics.mean_absolute_error(y_test, predicted))
print('Mean Squared Error:' , metrics.mean_squared_error(y_test, predicted))
print('Root Mean Squared Error:', math.sqrt(metrics.mean_squared_error(y_test, predicted)))

#Linear Regression
# Train the model on the whole dataset
regressor = LinearRegression()
regressor.fit(X, y)

# Predict the testing set
predicted = regressor.predict(X_test)

# add predicted column to dataset
dataset['Predicted'] = regressor.predict(X)

# print the evaluation metrics
print('Mean Absolute Error:' , metrics.mean_absolute_error(y_test, predicted))
print('Mean Squared Error:' , metrics.mean_squared_error(y_test, predicted))
print('Root Mean Squared Error:', math.sqrt(metrics.mean_squared_error(y_test, predicted)))

#Bar Graph comparing all parameters
import numpy as np
import matplotlib.pyplot as plt

# Evaluation metrics for linear regression model
linear_mae = 0.5017855048305236
linear_mse = 0.4796092073838382
linear_rmse = 0.6925382353226702

# Evaluation metrics for random forest model
rf_mae = 0.70734333566055
rf_mse = 1.0461219588154844
rf_rmse = 1.0228010357911672

# Create bar graph
labels = ['Linear Regression', 'Random Forest']
mae_values = [linear_mae, rf_mae]
mse_values = [linear_mse, rf_mse]
rmse_values = [linear_rmse, rf_rmse]

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, mae_values, width, label='Mean Absolute Error')
rects2 = ax.bar(x, mse_values, width, label='Mean Squared Error')
rects3 = ax.bar(x + width, rmse_values, width, label='Root Mean Squared Error')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Evaluation Metrics')
ax.set_title('Comparison of Linear Regression and Random Forest Models')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()

"""Based on the provided values, the Linear Regression model has a lower MAE, MSE, and
RMSE than the Random Forest model. This suggests that the Linear Regression model is
slightly more accurate in predicting the stock prices than the Random Forest model.

Stock recommandation Using Linear Regression
"""

tickers = ["AAPL", "MSFT", "META", "GOOGL", "JPM","PG", "MA", "AMZN", "NVDA", "KO"]
results = {}

for ticker in tickers:
    dataset = yf.Ticker(ticker)
    dataset = dataset.history(start="2018-01-01", end="2023-05-10")

    del dataset["Dividends"]
    del dataset["Stock Splits"]
    dataset.isnull().sum()

    X = dataset[['Open', 'High', 'Low', 'Volume']]
    y = dataset['Close']

    # Calculate the EMAs
    dataset['EMA50'] = dataset['Close'].ewm(span=50, adjust=False).mean()
    dataset['EMA200'] = dataset['Close'].ewm(span=200, adjust=False).mean()

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    # Train the model on the whole dataset
    regressor = LinearRegression()
    regressor.fit(X, y)

    # Predict the next trading day's closing price
    next_day = yf.download(ticker, period="2d")
    next_day_pred = regressor.predict(next_day.iloc[-2][['Open', 'High', 'Low', 'Volume']].values.reshape(1, -1))[0]
    print(f"\n\nSymbol: {ticker}")
    print('Next day predicted price:', next_day_pred)

    # add predicted column to dataset
    dataset['Predicted'] = regressor.predict(X)

    # Predict the testing set
    predicted = regressor.predict(X_test)

    # Create a dataframe for comparison
    dfr = pd.DataFrame({'Actual': y_test, 'Predicted': predicted})

    # Calculate annualized returns
    start_date = dataset.index.min()
    end_date = dataset.index.max()
    num_years = (end_date - start_date).days / 252
    annualized_return = (((y[-1] / y[0]) ** (1 / num_years)) - 1)*100
    formatted_return_percent = '{:.2f}'.format(annualized_return)

    # print the evaluation metrics
    print('Mean Absolute Error:' , metrics.mean_absolute_error(y_test, predicted))
    print('Mean Squared Error:' , metrics.mean_squared_error(y_test, predicted))
    print('Root Mean Squared Error:', math.sqrt(metrics.mean_squared_error(y_test, predicted)))
    # Print annualized returns
    print('Annualized Return:', formatted_return_percent)

    compare = dataset[['Close', 'Predicted', 'EMA50', 'EMA200']]
    print(compare)

    # plot actual v/s predicted line chart with EMAs
    fig = plt.figure(figsize=(12, 8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    compare[['Predicted', 'Close', 'EMA50', 'EMA200']].plot(kind='line', ax=ax, linewidth=0.75, 
    color={'Predicted': 'red', 'Close': 'blue', 'EMA50': 'green', 'EMA200': 'red'})
    ax.set_title(f'Actual v/s Predicted Stock Prices for {ticker}', fontsize=20, color='black')
    ax.set_facecolor('white')
    ax.set_xlabel('Date', fontsize=16, color='white')
    ax.set_ylabel('Closing Price', fontsize=16, color='white')
    ax.tick_params(axis='both', which='major', labelsize=12, color='black')
    labelcolor = 'black'
    ax.legend(['Close', 'Predicted', 'EMA50', 'EMA200'], fontsize=16)
    ax.set_xlim(pd.to_datetime('2021-01-01'), pd.to_datetime('2023-05-06'))
    plt.show()

    # store results
    results[ticker] = {
        'MAE': metrics.mean_absolute_error(y_test, predicted),
        'MSE': metrics.mean_squared_error(y_test, predicted),
        'RMSE': math.sqrt(metrics.mean_squared_error(y_test, predicted)),
        'Annualized Return': formatted_return_percent
    }

# compare results
df_results = pd.DataFrame.from_dict(results, orient='index')
df_results = df_results.sort_values(by=['RMSE'], ascending=True)
print('\nComparison of all stocks according to parameters:')
print(df_results)

# print top 4 stocks
top_4 = df_results.index[0:4]
print('\nTop 4 stocks:')
for ticker in top_4:
    print(ticker)

import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
# Loop over the top 4 stocks and create a candlestick chart for each of them
for ticker in top_4:

    # Load the data from Yahoo Finance
    df = yf.download(ticker, start='2022-12-01', end='2023-05-08')

    # Calculate the EMA values
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    df['EMA200'] = df['Close'].ewm(span=200).mean()

    # Add a new column for the date
    df['Date'] = df.index

    # Create the candlestick chart
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name=ticker)

    # Create the EMA lines
    ema50 = go.Scatter(x=df['Date'], y=df['EMA50'], name='EMA50', line=dict(color='green', width=1.5))
    ema200 = go.Scatter(x=df['Date'], y=df['EMA200'], name='EMA200', line=dict(color='red', width=1.5))

    # Combine the candlestick chart and EMA lines into one figure
    fig = go.Figure(data=[candlestick, ema50, ema200])

    # Customize the chart
    fig.update_layout(
        title=ticker,
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_white'
    )

    # Show the chart
    fig.show()

# create bar graph of stock vs annualized returns
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
df_results['Annualized Return'].str.rstrip('%').astype(float).plot(kind='bar', ax=ax)
ax.set_xticklabels(df_results.index, rotation=45)
ax.set_title('Annualized Returns by Stock', fontsize=16)
ax.set_xlabel('Stock', fontsize=14)
ax.set_ylabel('Annualized Return (%)', fontsize=14)
plt.show()

# allocate portfolio percentages
top_4 = df_results.index[0:4]

# calculate investment amount
investment_amount = 10000

# calculate allocation percentages based on annualized returns
most_accurate_stock = top_4[0]
most_accurate_percentage = 0.4
most_accurate_return = df_results.loc[most_accurate_stock, 'Annualized Return']
most_accurate_return = pd.to_numeric(most_accurate_return)
most_accurate_allocation = most_accurate_percentage * investment_amount
most_accurate_capital = most_accurate_allocation * (most_accurate_return / 100 + 1)

second_accurate_stock = top_4[1]
second_accurate_percentage = 0.3
second_accurate_return = df_results.loc[second_accurate_stock, 'Annualized Return']
second_accurate_return = pd.to_numeric(second_accurate_return)
second_accurate_allocation = second_accurate_percentage * investment_amount
second_accurate_capital = second_accurate_allocation * (second_accurate_return / 100 + 1)

third_accurate_stock = top_4[2]
third_accurate_percentage = 0.2
third_accurate_return = df_results.loc[third_accurate_stock, 'Annualized Return']
third_accurate_return = pd.to_numeric(third_accurate_return)
third_accurate_allocation = third_accurate_percentage * investment_amount
third_accurate_capital = third_accurate_allocation * (third_accurate_return / 100 + 1)

fourth_accurate_stock = top_4[3]
fourth_accurate_percentage = 0.1
fourth_accurate_return = df_results.loc[fourth_accurate_stock, 'Annualized Return']
fourth_accurate_return = pd.to_numeric(fourth_accurate_return)
fourth_accurate_allocation = fourth_accurate_percentage * investment_amount
fourth_accurate_capital = fourth_accurate_allocation * (fourth_accurate_return / 100 + 1)

# print allocation and capital for each stock
print(f"Investment in {most_accurate_stock}: ${most_accurate_allocation:.2f}, capital after 1 year: ${most_accurate_capital:.2f}")
print(f"Investment in {second_accurate_stock}: ${second_accurate_allocation:.2f}, capital after 1 year: ${second_accurate_capital:.2f}")
print(f"Investment in {third_accurate_stock}: ${third_accurate_allocation:.2f}, capital after 1 year: ${third_accurate_capital:.2f}")
print(f"Investment in {fourth_accurate_stock}: ${fourth_accurate_allocation:.2f}, capital after 1 year: ${fourth_accurate_capital:.2f}")
print()
#total Gain
total_capital_gain = (most_accurate_capital + second_accurate_capital + third_accurate_capital + fourth_accurate_capital) - investment_amount
total_gain = ((total_capital_gain+investment_amount) - investment_amount) / investment_amount * 100
print(f"Total capital gain after 1 year: {total_gain:.2f}%")

import matplotlib.pyplot as plt

# Define color palette
colors = ['#c9d9d3', '#e2d1c3', '#f2b5b8', '#e6f0cc']

# Define data
labels = [most_accurate_stock, second_accurate_stock, third_accurate_stock, fourth_accurate_stock]
sizes = [most_accurate_allocation, second_accurate_allocation, third_accurate_allocation, fourth_accurate_allocation]

# Create pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.axis('equal')
plt.title('Allocation of $10000 among top 4 stocks')

# Show plot
plt.show()

#total Gain
total_capital_gain = (most_accurate_capital + second_accurate_capital + third_accurate_capital + fourth_accurate_capital) - investment_amount
total_gain = ((total_capital_gain+investment_amount) - investment_amount) / investment_amount * 100
print(f"Total capital gain after 1 year: {total_gain:.2f}%")



import matplotlib.pyplot as plt

# Data
stocks = [most_accurate_stock, second_accurate_stock, third_accurate_stock, fourth_accurate_stock]
allocations = [most_accurate_allocation, second_accurate_allocation, third_accurate_allocation, fourth_accurate_allocation]
capitals = [most_accurate_capital, second_accurate_capital, third_accurate_capital, fourth_accurate_capital]

# Create Figure
fig, ax = plt.subplots(figsize=(8, 6))

# Bar Plot
bar_width = 0.35
x_pos = [i for i in range(len(stocks))]
ax.bar(x_pos, allocations, width=bar_width, label='Allocation', color='blue')
ax.bar([i + bar_width for i in x_pos], capitals, width=bar_width, label='Capital', color='orange')

# Set axis labels and title
ax.set_ylabel('Amount')
ax.set_xticks([i + bar_width / 2 for i in x_pos])
ax.set_xticklabels(stocks)
ax.set_title('Allocation and Capital for Each Stock')

# Add legend and grid
ax.legend()
ax.grid(True)

# Show plot
plt.show()