from flask.helpers import get_root_path
import dash
from dash import Dash, html
import logging
import dash_bootstrap_components as dbc
import os
from constants import log_key
from page.PageCallbacks import register_page3_callbacks
from page.PageDash import get_page3

logger = logging.getLogger(log_key)

class Callbacks:
    def __init__(self):
        self.default_app = None
        self.apps = dict()

    def apply_custom_index_string(self, app):
        app.index_string = '''
        <!DOCTYPE html>
        <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
            .chart_container: {
                display: flex;
                flexWrap: wrap;
                gap: 10px;
            }

            .chart-item {
                flex: 1 1 calc(50% - 10px);
                minWidth: 300px;
                width: 100%;
            }

            .dash-graph-wide {
                height: 60vh;
                width: 100%;
            }

            @media (min-width: 2000px) {
                .dash-graph-wide {
                    height: 30vh;
                }
            }

            /* Bootstrap Select Customization */
            .form-select {
                font-family: 'Gill Sans', sans-serif;
                border-radius: 4px;
                border: 1px solid #ced4da;
                padding: 0.375rem 2.25rem 0.375rem 0.75rem;
            }

            .form-select:focus {
                border-color: #80bdff;
                box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
            }

            /* Filter Container Styles */
            .filter-container {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 8px;
                margin-bottom: 2rem;
            }

            .filter-row {
                display: flex;
                gap: 1.5rem;
                align-items: flex-start;
                flex-wrap: wrap;
            }

            .filter-item {
                flex: 1;
                min-width: 200px;
            }

            .filter-label {
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #495057;
            }
            </style> 
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
        </html>
        '''

    def create_app(self, id, page_title, external_stylesheets=None):
        if external_stylesheets is None:
            external_stylesheets = [dbc.themes.BOOTSTRAP]
            
        self.apps[id] = Dash(
            name=page_title,
            requests_pathname_prefix=f"/{id}/",
            title=page_title,
            external_stylesheets=external_stylesheets,
        )

    def init_page3(self):
        key = "page3"
        self.create_app(
            key, 
            "Exposure Tool", 
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        app = self.apps["page3"]
        self.apps[key].layout = get_page3(app)
        self.apply_custom_index_string(app)
        register_page3_callbacks(app)

    def register_callbacks(self):
        self.default_app = Dash(
            name='Exposure Tool',
            requests_pathname_prefix='/',
            title="Exposure Tool",
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.init_page3()
        self.default_app.layout = get_page3(self.default_app)
        self.apply_custom_index_string(self.default_app)
        register_page3_callbacks(self.default_app)

def create_app():
    callbacks = Callbacks()
    callbacks.register_callbacks()
    return callbacks.default_app.server, callbacks.apps

if __name__ == '__main__':
    app, apps = create_app()
    app.run(debug=True)