# Page3Callbacks.py

def register_page3_callbacks(app):
    """Register callbacks for Page 3 (Exposure Tool)"""
    
    @app.callback(
        dash.Output("selection-checkbox-grid", "rowData"),
        [dash.Input('country-filter', 'value'),
         dash.Input('sector-filter', 'value')],
        prevent_initial_call=False  # Allow initial callback
    )
    def update_grid(selected_country, selected_sector):
        # Debug prints
        print(f"Page3 update_grid callback triggered")
        print(f"Selected country: {selected_country}")
        print(f"Selected sector: {selected_sector}")
        
        try:
            filtered_df = df.copy()
            
            if selected_country and selected_country != 'all':
                filtered_df = filtered_df[filtered_df['country_exposure_name'] == selected_country]
            if selected_sector and selected_sector != 'all':
                filtered_df = filtered_df[filtered_df['sector'] == selected_sector]
            
            print(f"Filtered dataframe shape: {filtered_df.shape}")
            return filtered_df.to_dict('records')
            
        except Exception as e:
            print(f"Error in update_grid: {str(e)}")
            # Return the original dataset on error
            return df.to_dict('records')

    @app.callback(
        dash.Output("download-dataframe-csv", "data"),
        [dash.Input("btn-download-csv", "n_clicks"),
         dash.Input("country-filter", "value"),
         dash.Input("sector-filter", "value")],
        prevent_initial_call=True
    )
    def download_csv(n_clicks, selected_country, selected_sector):
        if n_clicks is None:
            return None
            
        try:
            filtered_df = df.copy()
            if selected_country != 'all':
                filtered_df = filtered_df[filtered_df['country_exposure_name'] == selected_country]
            if selected_sector != 'all':
                filtered_df = filtered_df[filtered_df['sector'] == selected_sector]
            return dcc.send_data_frame(filtered_df.to_csv, "exposure_data.csv", index=False)
        except Exception as e:
            print(f"Error in download_csv: {str(e)}")
            return None




def init_page3(self):
    key = "page3"
    self.create_app(
        key, 
        "Exposure Tool", 
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, icon_css]
    )
    app = self.apps["page3"]
    app.use_pages = True
    app._suppress_callback_exceptions = True  # Add this line
    self.apps[key].layout = get_page3(app)
    self.apply_custom_index_string(app)
    register_page3_callbacks(app)



def get_page3(app):
    # Make sure df is properly imported here
    return dbc.Container(
        [
            html.H5("Exposure Tool", className="mb-3"),
            filter_row,
            html.Div(id='grid-container', children=[grid]),  # Wrap grid in a container
        ],
        className="dbc dbc-ag-grid",
        style={"marginTop": "20px"},
        fluid=True
    )


grid = html.Div([
    dag.AgGrid(
        id="selection-checkbox-grid",
        columnDefs=columnDefs,
        rowData=df.to_dict("records"),
        defaultColDef={"flex": 1, "minWidth": 150, "sortable": True, "resizable": True, "filter": True},
        dashGridOptions={
            'headerHeight': 50,
            "animateRows": False,
            'pagination': True,
            "paginationPageSize": 14,
            "suppressRowClickSelection": True,
        },
        className="ag-theme-alpine dbc-ag-grid",
        columnSize="sizeToFit",
        style={"height": "700px", "width": "100%", "--ag-header-background-color": "#F0F8FF"},
        dangerously_allow_code=True
    ),
    html.Div(id='grid-error-boundary')  # Add error boundary
])


app.clientside_callback(
    """
    function(n_intervals) {
        if (window.gridApi) {
            window.gridApi.sizeColumnsToFit();
        }
        return window.dash_clientside.no_update;
    }
    """,
    dash.Output('grid-container', 'children'),
    dash.Input('interval-component', 'n_intervals'),
    prevent_initial_call=True
)