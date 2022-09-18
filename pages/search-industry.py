import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Search Stock by Industry")
nasdaq_screener = pd.read_csv("data/nasdaq_screener.csv")

# get all nasdaq symbols
nasdaq_symbols = nasdaq_screener['Symbol'].tolist()
nasdaq_industries = nasdaq_screener['Industry'].tolist()
nasdaq_sectors = nasdaq_screener['Sector'].tolist()

selected_industries = st.multiselect("Pick industries", nasdaq_industries, default=["Electrical Products"])
selected_industries=["Electrical Products"]

# get yahoo data
df = pd.DataFrame()
for industry in selected_industries:
    ticker_industry = nasdaq_screener.loc[nasdaq_screener['Industry'] == industry]
    for ticker in ticker_industry['Symbol']:
        tick = yf.Ticker(ticker)
        tick_info = pd.DataFrame(list(tick.info.items()))
        transposed_tick_info = tick_info.T
        transposed_tick_info.rename(columns=transposed_tick_info.iloc[0], inplace=True)
        transposed_tick_info.drop([0], inplace=True)
        transposed_tick_info['Symbol'] = ticker
        df = pd.concat([df, transposed_tick_info], ignore_index=True)

final_output = nasdaq_screener.merge(df, how='inner', on='Symbol')

st.dataframe(final_output)
