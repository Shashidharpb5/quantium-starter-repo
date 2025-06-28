import pandas as pd
def test_data_load():
    df = pd.read_csv("formatted_data.csv")
    assert not df.empty, "Dataframe is empty"
    assert set(df.columns) == {"sales", "date", "region"}
def test_region_filter():
    df = pd.read_csv("formatted_data.csv")
    region = "north"
    filtered = df[df["region"] == region]
    assert all(filtered["region"] == region), "Region filter failed"
def test_date_format():
    df = pd.read_csv("formatted_data.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    assert not df["date"].isnull().any(), "Some date values could not be parsed"
def test_sales_column_numeric():
    df = pd.read_csv("formatted_data.csv")
    assert pd.api.types.is_numeric_dtype(df["sales"]), "Sales column is not numeric"
