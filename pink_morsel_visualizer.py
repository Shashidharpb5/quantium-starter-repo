import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load and sort data
DATA_PATH = "./formatted_data.csv"
data = pd.read_csv(DATA_PATH)
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values(by="date")

# Color palette
COLORS = {
    "primary": "#FEDBFF",
    "secondary": "#D598EB",
    "font": "#522A61"
}

# Initialize Dash app
dash_app = Dash(__name__)

# Header
header = html.H1(
    "Quantium Pink Morsel Sales Analysis",
    id="header",
    style={
        "background-color": COLORS["secondary"],
        "color": COLORS["font"],
        "padding": "20px",
        "border-radius": "10px",
        "textAlign": "center"
    }
)

# Region picker
region_picker = dcc.RadioItems(
    options=[
        {"label": "North", "value": "north"},
        {"label": "East", "value": "east"},
        {"label": "South", "value": "south"},
        {"label": "West", "value": "west"},
        {"label": "All", "value": "all"}
    ],
    value="all",
    id="region_picker",
    inline=True,
    style={"margin": "20px"}
)

# Visualization component
def generate_figure(filtered_data):
    fig = px.line(filtered_data, x="date", y="sales", title="Pink Morsel Sales Over Time")
    fig.update_layout(
        plot_bgcolor=COLORS["primary"],
        paper_bgcolor=COLORS["primary"],
        font_color=COLORS["font"]
    )
    fig.add_vline(x=pd.to_datetime("2021-01-15"), line_width=3, line_dash="dash", line_color="red")
    return fig

graph = dcc.Graph(id="visualization", figure=generate_figure(data))

# Layout
dash_app.layout = html.Div(
    children=[header, region_picker, graph],
    style={"padding": "30px", "background-color": COLORS["primary"]}
)

# Callback
@dash_app.callback(
    Output("visualization", "figure"),
    Input("region_picker", "value")
)
def update_chart(region):
    filtered = data if region == "all" else data[data["region"] == region]
    return generate_figure(filtered)

# Run server
if __name__ == "__main__":
    dash_app.run()
