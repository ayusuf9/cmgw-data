@app.callback(
    [Output('country-exposure-pct-graph', 'figure'),
    Output('country-exposure-revenue-graph', 'figure'),
    Output('security-alert', 'is_open'),
    Output('security-alert', 'children')],
    [Input('market-type-dropdown', 'value'),
    Input('exposure-type-dropdown', 'value'),
    Input('sector-dropdown', 'value'),
    Input('securities-dropdown', 'value')]
)
def update_graphs(market_type, countries, sector, securities):
    if securities is None or len(securities) == 0:
        return no_update, no_update, True, "Please select at least one security"
    elif len(securities) > 2:
        return no_update, no_update, True, "Maximum 2 securities allowed"

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
            if company_name in sector_mapping_one and sector_mapping_one[company_name] == sector:
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

    cg_color_pallet = {
        'sapphire': '#005F9E',
        'dark_sapphire': '#00294B',
        'ocean': '#009CDC',
        'light_ocean': '#7BD0E2',
        'turquoise': '#00AEA9',
        'dark_turquoise_1': '#008E77',
        'dark_turquoise_2': '#004C46',
        'raspberry': '#B42573',
        'dark_raspberry_1': '#762157',
        'dark_raspberry_2': '#532a45',
        'neutral_7': '#554742',
        'neutral_4': '#A39E99',
        'neutral_2': '#D5D0CA',
        'cg_recession': '#f3f3f3'
    }

    color_list = [
        cg_color_pallet['sapphire'],
        cg_color_pallet['turquoise'],
        cg_color_pallet['neutral_4'],
        cg_color_pallet['raspberry'],
        cg_color_pallet['dark_sapphire'],
        cg_color_pallet['light_ocean']
    ]

    def format_revenue(value):
        if abs(value) >= 1e12:
            return f"{value/1e12:.1f}T"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.1f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        else:
            return f"{value:.0f}"

    fig_pct = go.Figure()
    fig_revenue = go.Figure()

    if filtered_data.empty or not securities:
        return fig_pct, fig_revenue, True, "No data available for the selected filters."

    # Calculate data ranges with additional padding
    overall_pct_min = filtered_data['country_exposure_pct'].min()
    overall_pct_max = filtered_data['country_exposure_pct'].max()
    overall_revenue_min = filtered_data['country_exposure_revenue'].min()
    overall_revenue_max = filtered_data['country_exposure_revenue'].max()

    pct_padding = (overall_pct_max - overall_pct_min) * 0.40
    revenue_padding = (overall_revenue_max - overall_revenue_min) * 0.40

    pct_range = {
        'min': overall_pct_min - pct_padding,
        'max': overall_pct_max + pct_padding
    }
    revenue_range = {
        'min': max(0, overall_revenue_min - revenue_padding),
        'max': overall_revenue_max + revenue_padding
    }

    # Add border lines for percentage graph
    fig_pct.add_shape(
        type="line",
        x0=filtered_data['Date'].min() - pd.Timedelta(days=90),
        x1=filtered_data['Date'].max() + pd.Timedelta(days=90),
        y0=pct_range['max'],
        y1=pct_range['max'],
        yref="y2",
        line=dict(color="#7a7c7d", width=8),
        layer="below"
    )

    fig_pct.add_shape(
        type="line",
        x0=filtered_data['Date'].min() - pd.Timedelta(days=90),
        x1=filtered_data['Date'].max() + pd.Timedelta(days=90),
        y0=pct_range['min'],
        y1=pct_range['min'],
        yref="y2",
        line=dict(color="#7a7c7d", width=8),
        layer="below"
    )

    # Add border lines for revenue graph
    fig_revenue.add_shape(
        type="line",
        x0=filtered_data['Date'].min() - pd.Timedelta(days=90),
        x1=filtered_data['Date'].max() + pd.Timedelta(days=90),
        y0=revenue_range['max'],
        y1=revenue_range['max'],
        yref="y2",
        line=dict(color="#7a7c7d", width=8),
        layer="below"
    )

    fig_revenue.add_shape(
        type="line",
        x0=filtered_data['Date'].min() - pd.Timedelta(days=90),
        x1=filtered_data['Date'].max() + pd.Timedelta(days=90),
        y0=revenue_range['min'],
        y1=revenue_range['min'],
        yref="y",
        line=dict(color="#7a7c7d", width=8),
        layer="below"
    )

    for i, security in enumerate(securities):
        security_data = filtered_data[filtered_data['security_name'] == security]

        if len(security_data) == 0:
            continue

        def format_revenue_str(value):
            if abs(value) >= 1e9:
                return f"{value/1e9:.1f}B"
            elif abs(value) >= 1e6:
                return f"{value/1e6:.1f}M"
            else:
                return f"{value:.0f}"

        security_data['formatted_revenue'] = security_data['country_exposure_revenue'].apply(format_revenue_str)

        # Add percentage trace
        fig_pct.add_trace(go.Scatter(
            x=security_data['Date'],
            y=security_data['country_exposure_pct'],
            name=f"<b>{security}</b>",
            line=dict(
                shape='spline' if len(security_data) > 5 else 'linear',
                width=4.4,
                color=color_list[i % len(color_list)]
            ),
            mode='lines',
            yaxis='y2',
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Date: %{x|%Y-%m-%d}<br>"
                "Exposure: <b>%{y:.1f}%</b><br>"
                "<extra></extra>"
            )
        ))

        # Add revenue trace
        fig_revenue.add_trace(go.Scatter(
            x=security_data['Date'],
            y=security_data['country_exposure_revenue'],
            name=f"<b>{security}</b>",
            line=dict(
                shape='spline' if len(security_data) > 5 else 'linear',
                width=4.4,
                color=color_list[i % len(color_list)]
            ),
            mode='lines',
            yaxis='y2',
            customdata=np.stack((
                security_data['formatted_revenue'],
                security_data['isd_currency_symbol']
            ), axis=-1),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Date: %{x|%Y-%m-%d}<br>"
                "Revenue: <b>%{customdata[0]} %{customdata[1]}</b><br>"
                "<extra></extra>"
            )
        ))

    # Base layout configuration with range selector
    base_layout = dict(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Gill Sans', size=14),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family='Gill Sans',
        ),
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
            itemsizing='constant'
        ),
        margin=dict(t=120, r=70, l=70, b=50),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=2,
                         label="2y",
                         step="year",
                         stepmode="backward"),
                    dict(count=4,
                         label="4y",
                         step="year",
                         stepmode="backward"),
                    dict(count=6,
                         label="6y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all",
                         label="all")
                ]),
                bgcolor='#f8f9fa',
                font=dict(size=12),
                xanchor='left',
                x=0,
                y=1.1,
                activecolor='#dee2e6',
                bordercolor='#dee2e6',
                borderwidth=1
            ),
            type="date",
            tickfont=dict(weight='bold'),
            title_font=dict(weight='bold')
        )
    )

    # Update percentage figure layout
    fig_pct.update_layout(
        base_layout,
        title=dict(
            text="Exposure (Percentage)",
            font=dict(size=21, color="#00294b"),
            x=0.04
        ),
        yaxis2=dict(
            title="Exposure (%)",
            range=[overall_pct_min - pct_padding, overall_pct_max + pct_padding],
            tickformat=".1f",
            ticksuffix="%",
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=False,
            tickfont=dict(weight='bold'),
            title_font=dict(weight='bold')
        ),
        yaxis=dict(
            title="Exposure (%)",
            range=[overall_pct_min - pct_padding, overall_pct_max + pct_padding],
            tickformat=".1f",
            ticksuffix="%",
            overlaying='y2',
            side='right',
            showgrid=False,
            tickfont=dict(weight='bold'),
            title_font=dict(weight='bold')
        )
    )

    # Update revenue figure layout
    fig_revenue.update_layout(
        base_layout,
        title=dict(
            text="Revenue Exposure",
            font=dict(size=21, color="#00294b"),
            x=0.04
        ),
        yaxis2=dict(
            title="Revenue",
            range=[max(0, overall_revenue_min - revenue_padding),
                  overall_revenue_max + revenue_padding],
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=True,
            zerolinecolor='lightgray',
            zerolinewidth=1,
            tickfont=dict(weight='bold'),
            title_font=dict(weight='bold')
        ),
        yaxis=dict(
            title="Revenue",
            range=[max(0, overall_revenue_min - revenue_padding),
                  overall_revenue_max + revenue_padding],
            overlaying='y2',
            side='right',
            showgrid=False,
            tickfont=dict(weight='bold'),
            title_font=dict(weight='bold')
        )
    )

    return fig_pct, fig_revenue, False, ""

@app.callback(
    Output('download-csv', 'data'),
    Input('download-csv-button', 'n_clicks'),
    State('market-type-dropdown', 'value'),
    State('securities-dropdown', 'value'),
    prevent_initial_call=True
)
def download_csv(n_clicks, market_type, securities):
    if n_clicks is None or n_clicks == 0:
        return no_update
    filtered_data = data[(data['market_type'] == market_type) & (data['security_name'].isin(securities))]
    csv_data = filtered_data.to_csv(index=False)
    return {
        'content': csv_data,
        'filename': 'exposure_data.csv',
        'type': 'text/csv'
    }