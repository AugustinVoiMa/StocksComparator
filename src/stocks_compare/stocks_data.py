from enum import Enum

import yfinance as yf


class ScaleEnum(Enum):
    SCALE_1Y = "1y"


def retrieve_data(symbol, scale: ScaleEnum = ScaleEnum.SCALE_1Y):
    data = yf.download(symbol, start="2013-01-01", end="2024-12-31")

    if scale ==ScaleEnum.SCALE_1Y:
        data["Year"] = data.index.year
        close_col = "Adj Close" if "Adj Close" in data.columns else "Close"
        data = data.groupby("Year").last("Adj Close")[(close_col, symbol)]
        data.name = symbol
    else:
        raise Exception("Not Implemented")
    return data
