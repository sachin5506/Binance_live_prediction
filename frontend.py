import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------
# Function to get historical klines
# -----------------------------------
def get_historical_klines(symbol="BTCUSDT", interval="1m", start=None, end=None, limit=500):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    if start: params["startTime"] = start
    if end: params["endTime"] = end

    resp = requests.get(url, params=params)
    data = resp.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    num_cols = ["open","high","low","close","volume"]
    df[num_cols] = df[num_cols].astype(float)
    return df

# -----------------------------------
# Streamlit App UI
# -----------------------------------
st.title("📊 Binance API - Crypto Candlestick Data")

# Inputs
symbol = st.text_input("Trading Pair (e.g., BTCUSDT)", "BTCUSDT")
interval = st.selectbox("Interval", ["1m","5m","15m","1h","4h","1d"])
limit = st.slider("Number of candles", 10, 1000, 200)

# Fetch historical data
if st.button("Get Historical Data"):
    df = get_historical_klines(symbol, interval, limit=limit)
    st.write(f"Showing {len(df)} rows for {symbol} ({interval})")
    st.dataframe(df.tail(10))

    # Candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df['open_time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(title=f"{symbol} - {interval} Candlestick Data",
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
