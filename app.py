import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the formatted data
df = pd.read_csv("formatted_data.csv")
df['date'] = pd.to_datetime(df['date'])

# App Setup
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Poppins&display=swap']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Pink Morsel Sales Visualiser"

# App Layout
app.layout = html.Div([
    html.H1("Quantium Pink Morsel Sales Analysis", style={
        'textAlign': 'center',
        'color': '#880e4f',
        'fontFamily': 'Poppins'
    }),

    html.Div([
        html.Label("Filter by Region:", style={
            'fontSize': '18px',
            'marginRight': '10px',
            'fontWeight': 'bold',
            'color': '#37474f'
        }),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            inline=True,
            style={'fontSize': '16px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Graph(id='sales-line-graph'),

    html.Div("Created by Shashy 💡 | Quantium Data Challenge", style={
        'textAlign': 'center',
        'marginTop': '40px',
        'color': '#757575',
        'fontFamily': 'Poppins'
    })
], style={'padding': '40px'})


# Callback to update chart based on radio selection
@app.callback(
    Output('sales-line-graph', 'figure'),
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    filtered_df = df if selected_region == 'all' else df[df['region'] == selected_region]

    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title="Pink Morsel Daily Sales Over Time",
        labels={'date': 'Date', 'sales': 'Sales ($)'},
        markers=True
    )

    from datetime import datetime

    fig.add_vline(
        x=datetime(2021, 1, 15),
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    fig.update_layout(
        title_x=0.5,
        font=dict(family="Poppins", size=14),
        plot_bgcolor="#f8f8f8",
        hovermode='x unified'
    )
    return fig


# Run server
if __name__ == '__main__':
    app.run(debug=True)
