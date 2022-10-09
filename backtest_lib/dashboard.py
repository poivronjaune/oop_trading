from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

DASH_TITLE = "Maple Frog Stocks"

dash_view = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_view.title = DASH_TITLE

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

FOOTER_STYLE = {
    "position": "absolute", 
    "bottom": "0px",
}

EXCHANGES = ['NASDAQ', 'AMEX','ASX','LSE','NYSE','TSX','TSXV']
TIME_FRAMES = ['Daily','Hour','Minutes']

# Utility functions
def create_dropdown(id, val_list):
    id_str = id.replace('-select','')
    return html.Div([
        html.Div(id_str),
        dcc.Dropdown(val_list, val_list[0], id=id, clearable=False),
    ], style={"width":"200px"})

def create_ticker_input(id):
    return html.Div([
        html.Div("Ticker"),
        html.Div([
            dcc.Input(id=id, style={"width":"60%"}),
            dbc.Button("Update", color="primary", className="me-1"),
        ], style={"display":"flex", "margin":"auto", "justify-content":"normal"}),
    ], style={"background-color":"white", "width":"33%"})

header = dbc.Container([
    html.Div([
        html.H2(DASH_TITLE),
        html.H5(id="countup"),
    ], style={"display":"flex", "margin":"auto", "justify-content":"space-between"}),
    html.Hr()
])

footer = dbc.Container([
    html.Hr(),
    html.P("© 2022 Maple Frog Studio. All rights reserved.")
], style=FOOTER_STYLE)


inputs = dbc.Container([
    html.Div([
        create_dropdown(id='Exchange-select', val_list=EXCHANGES),
        create_dropdown(id='Timeframe-select', val_list=TIME_FRAMES),
        create_ticker_input(id='ticker'),
    ], style={"display":"flex", "margin":"auto", "justify-content":"space-around", "background-color":"white"})

])

graphs = dbc.Container([
    html.P("Graph boxes"),

    dcc.Interval(id="interval", interval=1500)
])

dash_view.layout = dbc.Container(
    [
        header,
        inputs,
        graphs,
        footer
    ]
)

@dash_view.callback(
    Output("countup", "children"),
    Input("interval", "n_intervals")
)
def counter(n_intervals):
    return str(n_intervals)



if __name__ == "__main__":
    dash_view.run_server(debug=True, port=8052)