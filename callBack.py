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