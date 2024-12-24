def register_page3_callbacks(app):
    @app.callback(
        Output('country-exposure-pct-graph', 'figure'),
        Output('country-exposure-revenue-graph', 'figure'),
        Output('security-alert', 'is_open'),
        Output('security-alert', 'children'),
        Input('market-type-dropdown', 'value'),
        Input('exposure-type-dropdown', 'value'),
        Input('sector-dropdown', 'value'),
        Input('securities-dropdown', 'value')
    )
    def update_graphs(market_type, countries, sector, securities):
        if securities is None or len(securities) == 0:
            return no_update, no_update, True, "Please select at least one security"
        elif len(securities) > 4:
            return no_update, no_update, True, "Maximum 4 securities allowed"

        if not isinstance(countries, list):
            countries = [countries]
            
        filtered_data = data[
            (data['market_type'] == market_type) &
            (data['country_exposure_name'].isin(countries)) &
            (data['security_name'].isin(securities))
        ]
        
        if sector:
            filtered_securities = []
            for security in securities:
                company_name = security.split(' (')[0]
                if company_name in sector_mapping and sector_mapping[company_name] == sector:
                    filtered_securities.append(security)
            filtered_data = filtered_data[filtered_data['security_name'].isin(filtered_securities)]

        filtered_data = (
            filtered_data.groupby(['security_name', 'Date'])
            .agg({
                'country_exposure_pct': 'sum',
                'country_exposure_revenue': 'sum',
                'isd_currency_symbol': 'first'
            })
            .reset_index()
        )

        # Rest of your existing update_graphs function remains the same
        # [Previous visualization code...]
        
        return fig_pct, fig_revenue, False, ""

    @app.callback(
        Output('securities-dropdown', 'options'),
        Output('securities-dropdown', 'value'),
        Input('market-type-dropdown', 'value'),
        Input('exposure-type-dropdown', 'value'),
        Input('sector-dropdown', 'value'),
        State('securities-dropdown', 'value')
    )
    def update_securities_dropdown(market_type, countries, sector, current_securities):
        if not isinstance(countries, list):
            countries = [countries]

        filtered_data = data[
            (data['market_type'] == market_type) &
            (data['country_exposure_name'].isin(countries))
        ]
        
        securities = filtered_data['security_name'].unique()
        
        if sector:
            filtered_securities = []
            for security in securities:
                company_name = security.split(' (')[0]
                if company_name in sector_mapping and sector_mapping[company_name] == sector:
                    filtered_securities.append(security)
            securities = filtered_securities

        options = [{'label': security, 'value': security} for security in securities]
        
        if current_securities:
            valid_securities = [s for s in current_securities if s in securities]
            if valid_securities:
                return options, valid_securities

        # Set default securities based on market type
        if market_type.lower() == "developed market":
            default_value = [s for s in ['Nvidia (2379504)', 'Qualcomm (2714923)'] if s in securities]
        elif market_type.lower() == "emerging market":
            default_value = [s for s in ['Lenovo Group (6218089)', 'Infosys (6205122)'] if s in securities]
        else:
            default_value = securities[:2].tolist() if len(securities) >= 2 else securities.tolist()
            
        return options, default_value

    return app