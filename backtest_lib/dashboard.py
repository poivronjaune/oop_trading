from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

DASH_TITLE = "Maple Frog Stock Screener"

dash_view = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_view.title = DASH_TITLE

def header():
    header = dbc.Container([
        html.H2(DASH_TITLE),
        html.Hr()
    ])
    return header 

def footer():
    footer = dbc.Container([
        html.Hr(),
        html.P("© 2022 Maple Frog Studio. All rights reserved.")
    ], style={
                "position": "absolute", 
                "bottom": "0px"
            })
    return footer

def inputs():
    inputs = dbc.Container([
        # TODO: use symbols exchange list
        dcc.Dropdown(['NASDAQ', 'AMEX','ASX','LSE','NYSE','TSX','TSXV'], 'NASDAQ', id='exchange-select'),
        dcc.Input(id='ticker'),
    ])
    return  inputs

def graphs():
    graphs = dbc.Container([
        html.P("Graph boxes")
    ])
    return graphs

dash_view.layout = dbc.Container(
    [
        header(),
        inputs(),
        graphs(),
        footer()
    ]
)

if __name__ == "__main__":
    dash_view.run_server(debug=True, port=8052)