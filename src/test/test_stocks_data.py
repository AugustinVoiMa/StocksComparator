import pandas as pd

from stocks_compare.stocks_data import retrieve_data


def test_retrieve_data():
    data1 = retrieve_data("FDJU.PA")
    data2 = retrieve_data("^FCHI")
    df = pd.DataFrame([data1, data2])
    print(df)
