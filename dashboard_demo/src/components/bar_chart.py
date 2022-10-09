from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from . import ids

MEDAL_DATA = px.data.medals_long()
print(MEDAL_DATA)

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.NATION_DROPDOWN, "value")
    )
    def update_bar_chart(nations: list[str]) -> html.Div:
        filtered_data = MEDAL_DATA.query("nation in @nations")
        if filtered_data.shape[0] == 0:
            return html.Div(children="No data selected")
        fig = px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
        
        return html.Div(
            id=ids.BAR_CHART,
            children=[
                dcc.Graph(figure=fig)
            ]
    )
    return html.Div(id=ids.BAR_CHART)