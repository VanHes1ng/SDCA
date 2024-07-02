import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from   matplotlib.colors import LinearSegmentedColormap
import streamlit as st


st.set_page_config("Long Term Investing Cypto", "📈", layout="wide", initial_sidebar_state="collapsed")

# Function to fetch historical data
def get_historical_data(symbol):
    data     = yf.download(symbol, period="max", interval='1d')
    df       = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    return df

# Fetch historical price data for the cryptocurrencies
price_data = pd.DataFrame()
data = get_historical_data("BTC-USD")
price_data["BTC-USD"] = data['Close']

# Calculate the 200-week period SMA for BTC
price_data["SMA_BTC"] = price_data["BTC-USD"].rolling(window=200*7).mean()

# Calculate the difference between BTC close price and its SMA
price_data['Diff']    = price_data['BTC-USD'] - price_data['SMA_BTC']

# Calculate the Z-score for the differences
price_data['Z_Diff']  = (price_data['Diff'] - price_data['Diff'].mean()) / price_data['Diff'].std()

# Create a custom colormap with three colors
colors           = [(0, 'purple'), (0.35, '#33cff6'), (1, 'red')]
n_bins           = 100  # Discretizes the interpolation into bins
three_color_cmap = LinearSegmentedColormap.from_list('three_color_gradient', colors, N=n_bins)

# Plot BTC close price and SMA with gradient color background based on Z-score
fig, ax = plt.subplots(figsize=(17, 8), dpi=500)

# Scatter plot with color based on Z-score
sc = ax.scatter(price_data.index, price_data['BTC-USD'],
                 c          = price_data['Z_Diff'], 
                 cmap       = three_color_cmap, 
                 alpha      = 0.8, 
                 edgecolor  = 'none')

# Plot the SMA line
ax.plot(price_data.index, price_data['SMA_BTC'], 
        label     = 'SMA 200', 
        color     = 'purple', 
        linewidth = 2)

# Add marks below bars where Z-score of difference is below -1
[c1, c2, c3, c4] = st.columns([1, 10, 4, 1])
c3.write("#")
c3.write("###")

c3.markdown("""<hr style="height:4px;border:none;color:#333;background-color:#1d9ff0;" /> """, unsafe_allow_html=True)



below_threshold = price_data['Z_Diff'] < c3.number_input("Threshold for SDCA IN", -1.0, -0.5, -0.7, 0.1)
above_threshold = price_data['Z_Diff'] > c3.number_input("Threshold for SDCA OUT", 0.0, 4.0, 2.0, 0.1)
ax.scatter(price_data.index[below_threshold], price_data['BTC-USD'][below_threshold]*0.7,
            color       = '#2788e8', 
            marker      = 'D', 
            label       = 'DCA IN', 
            edgecolor   = 'none')

ax.scatter(price_data.index[above_threshold], price_data['BTC-USD'][above_threshold]*1.35,
            color       = 'red', 
            marker      = 'v', 
            label       = 'DCA OUT', 
            edgecolor   = 'none')

# Add colorbar
cbar = plt.colorbar(sc, ax=ax)

z_val = price_data['Z_Diff']*-1
cbar.set_label('Z-score of Difference')

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.set_yscale('log')
ax.set_title('BTC Close Price with SMA 200 and Z-score Based Gradient')
ax.legend()


with c2:
    st.title("Crypto SDCA System")
    st.markdown("""<hr style="height:4px;border:none;color:#333;background-color:#1d9ff0;" /> """, unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)

with c3:
    st.subheader("How it Works?")
    st.write('''

The Crypto SDCA System automates cryptocurrency investment decisions using systematic dollar-cost averaging (SDCA) principles. 

It utilizes historical price data to compute the **200-week Simple Moving Average (SMA)**, assesses deviations from this trend using **Z-score** calculations, 
and visualizes price trends with gradient colors. 

    
:blue[◆] Buy signals are identified when the Z-score drops below **"Threshold for SDCA IN" -0.70**. 

:red[▼] Sell signals trigger when it exceeds **"Threshold for SDCA OUT" +2.0**, 
aiming for disciplined, data-driven investment strategies.

''')

c2.write("#")
c2.write("""
        ### Disclaimer:

This system is for informational purposes only and should not be considered financial advice. 
Investors should conduct their own research or consult with a financial advisor before making investment decisions.""")

with st.sidebar:
    st.write("""
### About
             
    𝗞𝗘𝗬 𝗙𝗘𝗔𝗧𝗨𝗥𝗘𝗦:

- **Data Source**: Utilizes Yahoo Finance to fetch historical price data for cryptocurrencies.
- **Indicator Calculation**: Computes the 200-week Simple Moving Average (SMA) to gauge long-term price trends.
- **Difference Calculation**: Measures the difference between current prices and the SMA to assess deviations.
- **Z-score Calculation**: Normalizes the difference using Z-score, indicating deviations from the SMA trend.
- **Gradient Color Visualization**: Visualizes price trends with a gradient color background based on Z-score values.
- **Threshold-based Alerts**: Marks potential entry points (buy signals) when the Z-score falls below -0.70, and exit points (sell signals) when it rises above +2.00.

*This system aims to provide objective investment decisions, reduce emotional bias, and optimize cryptocurrency investments over the long term.*

---
- **GitHub:**      https://github.com/VanHes1ng
- **TradingView:** https://www.tradingview.com/u/VanHe1sing/
- **Twitter:**     https://x.com/sxJEoRg7wwLR6ug       
- **Telegram:**    t.me/IvanKocherzhat

## Crated by @VanHelsing
                  
             """)