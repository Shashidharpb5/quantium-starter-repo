import csv
import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

# === Step 1: Prepare CSV data ===
DATA_DIRECTORY = "./data"
OUTPUT_FILE_PATH = "./formatted_data.csv"

with open(OUTPUT_FILE_PATH, "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["sales", "date", "region"])  # header

    for file_name in os.listdir(DATA_DIRECTORY):
        if file_name.endswith(".csv"):
            with open(f"{DATA_DIRECTORY}/{file_name}", "r") as input_file:
                reader = csv.reader(input_file)
                next(reader)  # skip header
                for row in reader:
                    product, raw_price, quantity, date, region = row
                    if product == "pink morsel":
                        price = float(raw_price[1:])  # remove $
                        sale = price * int(quantity)
                        writer.writerow([sale, date, region])

# === Step 2: Load and clean CSV for Dash ===
df = pd.read_csv(OUTPUT_FILE_PATH)

# Force correct datatypes
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df.dropna(subset=["date", "sales"], inplace=True)

# Group by date
daily_sales = df.groupby("date")["sales"].sum().reset_index()

# === Step 3: Build Dash app ===
app = dash.Dash(__name__)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily_sales["date"],
    y=daily_sales["sales"],
    mode="lines+markers",
    name="Daily Sales"
))

# Add vertical line for Jan 15, 2021
fig.add_shape(
    type="line",
    x0="2021-01-15", x1="2021-01-15",
    y0=0, y1=daily_sales["sales"].max(),
    line=dict(color="red", width=2, dash="dash")
)

fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["sales"].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

fig.update_layout(
    title="Pink Morsel Daily Sales Over Time",
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    template="plotly_white"
)

app.layout = html.Div(children=[
    html.H1("Quantium Pink Morsel Sales Analysis", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
