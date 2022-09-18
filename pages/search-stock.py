import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Search Stock by Name")
nasdaq_screener = pd.read_csv("data/nasdaq_screener.csv")

nasdaq_symbols = nasdaq_screener['Symbol'].tolist()

dropdown = st.multiselect("Pick stocks", nasdaq_symbols, default=["AAPL", "AMZN", "META", "TSLA", "GOOG", "MSFT"])

# nasdaq data
selected_tickers = nasdaq_screener.loc[nasdaq_screener['Symbol'].isin(dropdown)]
selected_columns = selected_tickers[['Symbol', 'Name', 'IPO Year']]
selected_columns['IPO Year'] = selected_columns['IPO Year'].astype(int)

# yahoo finance data
df = pd.DataFrame()
for ticker in dropdown:
    tick = yf.Ticker(ticker)
    tick_info = pd.DataFrame(list(tick.info.items()))
    transposed_tick_info = tick_info.T
    transposed_tick_info.rename(columns=transposed_tick_info.iloc[0], inplace=True)
    transposed_tick_info.drop([0], inplace=True)
    transposed_tick_info['Symbol'] = ticker
    df = pd.concat([df, transposed_tick_info], ignore_index=True)

final_output = selected_columns.merge(df, how='inner', on='Symbol')


st.dataframe(final_output)

#
# start = st.date_input("Start", value=pd.to_datetime("2020-01-01"))
# end = st.date_input("End", value=pd.to_datetime("today"))
#
#
# if len(dropdown) > 0:
#     df = yf.download(dropdown, start, end)['Adj Close']
#     st.header("Adjusted Closing of {}".format(dropdown))
#     st.line_chart(df)

