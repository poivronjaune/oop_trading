from dash import Dash, html, dcc

from . import ids

def render(app: Dash, all_exchanges) -> html.Div:
    print(type(all_exchanges))
    return html.Div(
        children=[
            html.H6("Exchange"),
            dcc.Dropdown(
                id=ids.EXCHANGE_DROPDOWN,
                multi=False,
                options=[{'label': exchange.get('Name'), "value": exchange.get('Code')} for exchange in all_exchanges],
                value=all_exchanges[0].get('Code'),
                searchable=False,
                clearable=False
            )
        ]
    )