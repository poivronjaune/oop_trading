from dash import Dash, html

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="header",
        children=[
            html.H2(app.title),
            html.Hr(),
            children=[
                classname="header-container",
                children = [
                    #TODO: ICICI
                ]
            ]
        ]
    )