from dash import Dash, html

from . import exchange_dropdown

def create_layout(app: Dash, data) -> html.Div:
    # Seperate data structure into logical chuncks
    exchanges = data.get('exchanges')

    return html.Div(
        className='container',
        children=[
            app.title,
            html.Hr(),
            html.Div(
                className='filter_inputs',
                children=[
                    exchange_dropdown.render(app, exchanges)
                ], style={'display':'flex'}
            )
        ],
    )




