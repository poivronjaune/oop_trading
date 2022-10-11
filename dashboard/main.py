from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout

def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Maple Frog Dashboard"
    app.layout = create_layout(app)
    app.run_server(debug=True, port=8052)

if __name__ == "__main__":
    main()