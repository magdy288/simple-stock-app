## imports
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta


## Fetching stock data
def get_data(symbol):

    ticker = yf.Ticker(symbol)
    bars = ticker.history()

    df = pd.DataFrame(bars)

    # df['Date'] = pd.to_datetime(df['Date'])
    # df.set_index('Date', inplace=True)

    return df


## Calculate indicators(rsi, atr)
def get_indicators(df):
    rsi = ta.rsi(df['Close'], length=14)

    atr = ta.atr(df['High'], df['Low'], df['Close'], length=5)

    return rsi, atr


## create our main app
def app():
    st.set_page_config(page_title='Stock Dashboard', layout='wide', page_icon="📈")
    hide_menu_style = "<style> footer {visibility: hidden;} </style>"
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    st.title("📈 Stock Dashboard")
    popular_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB','NVDA','JPM']
    symbol = st.sidebar.selectbox('Select a stock symbol:', popular_symbols, index=2)


    ## Displaying stock data
    if symbol:
        df = get_data(symbol)

        if df is not None:
            rsi, atr = get_indicators(df)

    ## Displaying metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Close Price', f'{df['Close'].iloc[-1]}')
    with col2:
        st.metric('RSI Value:', f'{rsi.iloc[-1]}')
    with col3:
        st.metric('ATR Value', f'{atr.iloc[-1]}')

    ## CandleStick Chart
    st.subheader('Candlestick Chart')
    candle_chart = go.Figure(data=[go.Candlestick(
        x=df.index, 
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    candle_chart.update_layout(title=f'{symbol} Candlestick Chart', xaxis_rangeslider_visible=False)

    st.plotly_chart(candle_chart, use_container_width=True)

    ## Summary and data export
    st.subheader('Summary')
    st.dataframe(df.tail())

    st.download_button('Download Stock Data Overview', df.to_csv(index=True))



## Running the Function
if __name__ == '__main__':
    app()

# df = get_data('AAPL')

# print(df.head(10))