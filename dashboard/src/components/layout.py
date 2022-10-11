from dash import Dash, html


def create_layout(app: Dash, symbols_data) -> html.Div:
    return html.Div(
        className='container',
        children=[
            app.title,
            html.Hr()
        ],
    )




