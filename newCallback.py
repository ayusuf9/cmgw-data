# from dash.dependencies import Input, Output, State
# import plotly.graph_objects as go
# import pandas as pd
# from dash import no_update
# import datetime

# # Load and preprocess data
# data = pd.read_csv('pages/Page3/updated_data.csv')
# data['Date'] = pd.to_datetime(data['month_date'])
# data['security_name'] = data['security_name'].astype('category')
# data['iso_country_symbol'] = data['iso_country_symbol'].astype('category')
# data['market_type'] = data['market_type'].astype('category')
# data['sedol'] = data['sedol'].astype('category')
# data['security_name'] = data['security_name'] + ' (' + data['sedol'] + ')'

# data = data[data['security_name'] != '3I Group (B1YW440)']
# data['Year'] = data['Date'].dt.year
# securities_with_data = data['security_name'].tolist()
# data = data[data['security_name'].isin(securities_with_data)]
# data['country_exposure_pct'] = data['country_exposure(pct)']

# # Load sector data
# sector_data = pd.read_csv('pages/Page3/updated_ch_hk_data.csv')
# sector_mapping = dict(zip(sector_data['companyname'], sector_data['sector']))

# def register_page3_callbacks(app):
#     @app.callback(
#         Output('exposure-type-dropdown', 'options'),
#         Output('exposure-type-dropdown', 'value'),
#         Input('market-type-dropdown', 'value')
#     )
#     def update_country_dropdown(market_type):
#         countries = data[data['market_type'] == market_type]['country_exposure_name'].unique()
#         options = [{'label': country.title(), 'value': country} for country in countries]
#         default_countries = ['China', 'Hong Kong']
#         default_value = [country for country in default_countries if country in countries]
#         if not default_value:
#             default_value = countries[:2].tolist() if len(countries) >= 2 else countries.tolist()
#         return options, default_value

#     @app.callback(
#         Output('sector-dropdown', 'options'),
#         Output('sector-dropdown', 'value'),
#         Input('market-type-dropdown', 'value'),
#         Input('exposure-type-dropdown', 'value')
#     )
#     def update_sector_dropdown(market_type, countries):
#         if not isinstance(countries, list):
#             countries = [countries]
        
#         filtered_securities = data[
#             (data['market_type'] == market_type) &
#             (data['country_exposure_name'].isin(countries))
#         ]['security_name'].unique()
        
#         available_sectors = set()
#         for security in filtered_securities:
#             company_name = security.split(' (')[0]
#             if company_name in sector_mapping:
#                 available_sectors.add(sector_mapping[company_name])
        
#         options = [{'label': sector, 'value': sector} for sector in sorted(available_sectors)]
#         default_value = list(sorted(available_sectors))[0] if available_sectors else None
        
#         return options, default_value

#     @app.callback(
#         Output('securities-dropdown', 'options'),
#         Output('securities-dropdown', 'value'),
#         Input('market-type-dropdown', 'value'),
#         Input('exposure-type-dropdown', 'value'),
#         Input('sector-dropdown', 'value'),
#         State('securities-dropdown', 'value')
#     )
#     def update_securities_dropdown(market_type, countries, sector, current_securities):
#         if not isinstance(countries, list):
#             countries = [countries]
        
#         filtered_data = data[
#             (data['market_type'] == market_type) &
#             (data['country_exposure_name'].isin(countries))
#         ]
        
#         securities = filtered_data['security_name'].unique()
        
#         if sector:
#             filtered_securities = []
#             for security in securities:
#                 company_name = security.split(' (')[0]
#                 if company_name in sector_mapping and sector_mapping[company_name] == sector:
#                     filtered_securities.append(security)
#             securities = filtered_securities

#         options = [{'label': security, 'value': security} for security in securities]
        
#         if current_securities:
#             valid_securities = [s for s in current_securities if s in securities]
#             if valid_securities:
#                 return options, valid_securities

#         if market_type.lower() == "developed market":
#             default_value = [s for s in ['Nvidia (2379504)', 'Qualcomm (2714923)'] if s in securities]
#         elif market_type.lower() == "emerging market":
#             default_value = [s for s in ['Lenovo Group (6218089)', 'Infosys (6205122)'] if s in securities]
#         else:
#             default_value = securities[:2].tolist() if len(securities) >= 2 else securities.tolist()
            
#         return options, default_value

#     @app.callback(
#         [Output('country-exposure-pct-graph', 'figure'),
#          Output('country-exposure-revenue-graph', 'figure'),
#          Output('security-alert', 'is_open'),
#          Output('security-alert', 'children')],
#         [Input('market-type-dropdown', 'value'),
#          Input('exposure-type-dropdown', 'value'),
#          Input('sector-dropdown', 'value'),
#          Input('securities-dropdown', 'value')]
#     )
#     def update_graphs(market_type, countries, sector, securities):
#         if securities is None or len(securities) == 0:
#             return no_update, no_update, True, "Please select at least one security"
#         elif len(securities) > 4:
#             return no_update, no_update, True, "Maximum 4 securities allowed"

#         if not isinstance(countries, list):
#             countries = [countries]

#         filtered_data = data[
#             (data['market_type'] == market_type) &
#             (data['country_exposure_name'].isin(countries)) &
#             (data['security_name'].isin(securities))
#         ]
        
#         if sector:
#             filtered_securities = []
#             for security in securities:
#                 company_name = security.split(' (')[0]
#                 if company_name in sector_mapping and sector_mapping[company_name] == sector:
#                     filtered_securities.append(security)
#             filtered_data = filtered_data[filtered_data['security_name'].isin(filtered_securities)]

#         filtered_data = (
#             filtered_data.groupby(['security_name', 'Date'])
#             .agg({
#                 'country_exposure_pct': 'sum',
#                 'country_exposure_revenue': 'sum',
#                 'isd_currency_symbol': 'first'
#             })
#             .reset_index()
#         )

#         cg_color_pallet = {
#             'sapphire': '#005F9E',
#             'dark_sapphire': '#00294B',
#             'ocean': '#009CDC',
#             'light_ocean': '#7BD0E2',
#             'turquoise': '#00AEA9',
#             'dark_turquoise_1': '#008E77',
#             'dark_turquoise_2': '#004C46',
#             'raspberry': '#B42573',
#             'dark_raspberry_1': '#762157',
#             'dark_raspberry_2': '#532a45',
#             'neutral_7': '#554742',
#             'neutral_4': '#A39E99',
#             'neutral_2': '#D5D0CA',
#             'cg_recession': '#f3f3f3'
#         }

#         color_list = [
#             cg_color_pallet['sapphire'],
#             cg_color_pallet['turquoise'],
#             cg_color_pallet['neutral_4'],
#             cg_color_pallet['raspberry'],
#             cg_color_pallet['dark_sapphire'],
#             cg_color_pallet['light_ocean']
#         ]

#         def format_revenue(value):
#             if abs(value) >= 1e12:
#                 return f"{value/1e12:.1f}T"
#             elif abs(value) >= 1e9:
#                 return f"{value/1e9:.1f}B"
#             elif abs(value) >= 1e6:
#                 return f"{value/1e6:.1f}M"
#             else:
#                 return f"{value:.0f}"

#         fig_pct = go.Figure()
#         fig_revenue = go.Figure()
        
#         overall_pct_min = float('inf')
#         overall_pct_max = float('-inf')
#         overall_revenue_min = float('inf')
#         overall_revenue_max = float('-inf')

#         for i, security in enumerate(securities):
#             security_data = filtered_data[filtered_data['security_name'] == security]

#             overall_pct_min = min(overall_pct_min, security_data['country_exposure_pct'].min())
#             overall_pct_max = max(overall_pct_max, security_data['country_exposure_pct'].max())
#             overall_revenue_min = min(overall_revenue_min, security_data['country_exposure_revenue'].min())
#             overall_revenue_max = max(overall_revenue_max, security_data['country_exposure_revenue'].max())

#             fig_pct.add_trace(go.Scatter(
#                 x=security_data['Date'],
#                 y=security_data['country_exposure_pct'],
#                 name=f"<b>{security}</b>",
#                 line=dict(shape='spline', width=4.5, color=color_list[i % len(color_list)]),
#                 mode='lines',
#                 showlegend=True,
#                 marker=dict(symbol=i),
#                 yaxis='y2',
#                 hovertemplate=(
#                     "<b>%{fullData.name}</b><br>"
#                     "Date: %{x|%Y-%m-%d}<br>"
#                     "Exposure: <b>%{y:.2f}%</b><br>"
#                     "<extra></extra>"
#                 )
#             ))

#             fig_revenue.add_trace(go.Scatter(
#                 x=security_data['Date'],
#                 y=security_data['country_exposure_revenue'],
#                 name=f"<b>{security}</b>",
#                 line=dict(shape='spline', width=4.5, color=color_list[i % len(color_list)]),
#                 mode='lines',
#                 showlegend=True,
#                 marker=dict(symbol=i),
#                 yaxis='y2',
#                 customdata=security_data['isd_currency_symbol'],
#                 hovertemplate=(
#                     "<b>%{fullData.name}</b><br>"
#                     "Date: %{x|%Y-%m-%d}<br>"
#                     "Revenue: <b>" + security_data['country_exposure_revenue'].apply(format_revenue) + " " + 
#                     security_data['isd_currency_symbol'] + "</b><br>"
#                     "<extra></extra>"
#                 )
#             ))

#         layout_updates = dict(
#             hoverlabel=dict(
#                 bgcolor="white",
#                 font_size=12,
#                 font_family='Gill Sans'
#             ),
#             hovermode="closest",
#             legend=dict(
#                 orientation="h",
#                 yanchor="bottom",
#                 y=1.02,
#                 xanchor="right",
#                 x=1,
#                 font=dict(
#                     family='Gill Sans',
#                     size=11,
#                     color="#5a5a5a"
#                 ),
#                 itemsizing='constant',
#                 itemwidth=30
#             ),
#             margin=dict(t=120, r=20, l=20, b=50)
#         )

#         fig_pct.update_layout(**layout_updates)
#         fig_revenue.update_layout(**layout_updates)

#         pct_range = overall_pct_max - overall_pct_min
#         revenue_range = overall_revenue_max - overall_revenue_min

#         fig_pct.add_hline(y=overall_pct_max + 0.1 * pct_range, line=dict(color='gray', width=4), opacity=0.7)
#         fig_pct.add_hline(y=overall_pct_min - 0.1 * pct_range, line=dict(color='gray', width=4), opacity=0.7)

#         fig_revenue.add_hline(y=overall_revenue_max + 0.1 * revenue_range, line=dict(color='gray', width=4), opacity=0.7)
#         fig_revenue.add_hline(y=-0.1, line=dict(color='gray', width=4), opacity=0.7)

#         def get_date_range(fig, days):
#             max_date = max(max(trace.x) for trace in fig.data if len(trace.x) > 0)
#             x_data = fig.data[0].x
#             start_date = max(min(x_data), max_date - pd.Timedelta(days=days))
#             return [start_date, max_date]

#         for fig in [fig_pct, fig_revenue]:
#             max_date = max(max(trace.x) for trace in fig.data if len(trace.x) > 0)
#             initial_range = [max_date - pd.Timedelta(days=365*3), max_date]

#             fig.update_layout(
#                 xaxis=dict(
#                     range=initial_range,
#                     tickfont=dict(
#                         family='Gill Sans',
#                         size=15,
#                         color='#00003f',
#                         weight='bold'
#                     ),
#                     showgrid=False,
#                     ticks="outside"
#                 ),
#                 updatemenus=[
#                     dict(
#                         type="buttons",
#                         showactive=True,
#                         active=0,
#                         buttons=[
#                             dict(
#                                 label="3Y",
#                                 method="relayout",
#                                 args=[{"xaxis.range": get_date_range(fig, 365*3)}]
#                             ),
#                             dict(
#                                 label="5Y",
#                                 method="relayout",
#                                 args=[{"xaxis.range": get_date_range(fig, 365*5)}]
#                             ),
#                             dict(
#                                 label="All",
#                                 method="relayout",
#                                 args=[{"xaxis.autorange": True}]
#                             ),
#                         ],
#                         direction="right",
#                         pad={"r": 10, "t": 10, "b": 10, "l": 10},
#                         x=0,
#                         xanchor="left",
#                         y=1.14,
#                         yanchor="top",
#                         bgcolor="white",
#                         bordercolor="rgba(100, 149, 237, 0.7)",
#                         borderwidth=1.3,
#                         font=dict(family="Gill Sans", size=12, color="black")
#                     )
#                 ]
#             )

#         # Update specific layouts for each figure
#         fig_pct.update_layout(
#             title=dict(
#                 text="Exposure (Percentage)",
#                 font=dict(size=21, color="#00294b", weight='bold'),
#                 x=0.04
#             ),
#             yaxis=dict(
#                 title=dict(
#                     text="Exposure",
#                     font=dict(family='Gill Sans', size=15, color="#00003f", weight='bold')
#                 ),
#                 showline=False,
#                 zeroline=False,
#                 showgrid=False,
#                 ticks="outside",
#                 ticklen=5,
#                 tickformat=".0f",
#                 tickprefix='',
#                 ticksuffix='%',
#                 tickfont=dict(family='Gill Sans', size=15, color='