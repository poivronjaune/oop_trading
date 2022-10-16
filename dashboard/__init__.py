from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from .src.components.layout import create_layout

class Dashboard():
    def __init__(self, data) -> None:
        self.app = Dash(external_stylesheets=[BOOTSTRAP])
        self.app.title = "Maple Frog Dashboard"
        self.data = data
        
    def run(self) -> None:
        self.app.layout = create_layout(self.app, self.data)
        self.app.run_server(debug=True, port=8052)

