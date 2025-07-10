from enum import Enum

import pandas as pd
import streamlit as st
import yfinance as yf


class ScaleEnum(Enum):
    SCALE_1Y = "1y"


def retrieve_data(symbol, scale: ScaleEnum = ScaleEnum.SCALE_1Y):
    data = yf.download(symbol, start="2013-01-01", end="2024-12-31")

    if scale == ScaleEnum.SCALE_1Y:
        data["Year"] = data.index.year
        close_col = "Adj Close" if "Adj Close" in data.columns else "Close"
        data = data.groupby("Year").last("Adj Close")[(close_col, symbol)]
        data.name = symbol
    else:
        raise Exception("Not Implemented")
    return data


st.title("Stocks comparator")


@st.dialog("Select the Stock")
def select_stock(stock_id):
    search_str = st.text_input("Search:", placeholder="Name, isin, symbol, ...")
    if search_str != "":

        result = yf.search.Search(search_str)

        options = [r["symbol"] for r in result.quotes]
        captions = [f"{r.get('shortname', 'n/a')} ({r.get('exchange', 'n/a')})" for r in result.quotes]

        selected = st.radio("Select the right stock",
                            options, captions=captions,
                            index=None
                            )

        if selected in options:
            idx = options.index(selected)
            st.session_state[stock_id] = {'symbol': selected, 'name': result.quotes[idx]["shortname"]}
            st.rerun()


data1 = data2 = None

if st.session_state.get("stock1") is not None:
    st.write(f"Stock 1: {st.session_state.stock1['name']} ({st.session_state.stock1['symbol']})")
    data1 = retrieve_data(st.session_state.stock1['symbol'])
if st.button("Select Stock 1"):
    select_stock("stock1")

if st.session_state.get("stock2") is not None:
    st.write(f"Stock 2: {st.session_state.stock2['name']} ({st.session_state.stock2['symbol']})")
    data2 = retrieve_data(st.session_state.stock2['symbol'])
if st.button("Select Stock 2"):
    select_stock("stock2")

all_data = [d for d in [data1, data2] if d is not None]

if len(all_data):
    df = pd.DataFrame(all_data, index=[d.name for d in all_data]).T
    print("raw", df)
    df = df.pct_change() * 100
    print("return", df)
    st.bar_chart(df, x=None, y=df.columns, stack=False)
