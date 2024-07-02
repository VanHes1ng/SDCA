import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

# Function to fetch historical data
def get_historical_data(symbol):
    data = yf.download(symbol, period="6000d", interval='1d')
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    return df

# Fetch historical price data for the cryptocurrencies
price_data = pd.DataFrame()
data = get_historical_data("BTC-USD")
price_data["BTC-USD"] = data['Close']

# Calculate the SMA for BTC
price_data["SMA_BTC"] = price_data["BTC-USD"].rolling(window=200*7).mean()

# Calculate the difference between BTC close price and its SMA
price_data['Diff'] = price_data['BTC-USD'] - price_data['SMA_BTC']

# Calculate the Z-score for the differences
price_data['Z_Diff'] = (price_data['Diff'] - price_data['Diff'].mean()) / price_data['Diff'].std()

# Plot BTC close price and SMA with gradient color background based on Z-score
fig, ax = plt.subplots(figsize=(14, 7))

# Scatter plot with color based on Z-score
sc = ax.scatter(price_data.index, price_data['BTC-USD'], c=price_data['Z_Diff'], cmap='coolwarm', alpha=0.6, edgecolor='none')

# Plot the SMA line
ax.plot(price_data.index, price_data['SMA_BTC'], label='SMA 200', color='black', linewidth=2)

# Add colorbar
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Z-score of Difference')

# Add marks below bars where Z-score of difference is below -1
below_threshold = price_data['Z_Diff'] < -0.75
ax.scatter(price_data.index[below_threshold], price_data['BTC-USD'][below_threshold]*0.8, color='green', marker='^', label='Z_Diff < -0.75', edgecolor='none')

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.set_yscale('log')
ax.set_title('BTC Close Price with SMA 200 and Z-score Based Gradient')
ax.legend()

plt.show()