import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def get_data():
    data = pd.read_csv('pages/Page3/updated_data.csv')
    return data

def get_sectors():
    data = get_data()
    return sorted(data['sector'].unique())

def get_defaults():
    data = get_data()
    market_types = data['market_type'].unique()
    default_market_type = market_types[1]
    default_securities = data[data['market_type'] == default_market_type]['security_name'].unique()[-2:]
    return default_market_type, default_securities

def get_page3(app):
    dfa = pd.read_csv('pages/Page3/updated_ch_hk_data.csv')
    df = dfa[['companyname', 'sector', 'total_revenue', 'china_plus_hk_rev', 'china_plus_hk_pct']]
    df.columns = ['Company Name', 'Sector', 'Total Revenue', 'CH, HK Revenue', 'CH, HK Percentage']

    data = pd.read_csv('pages/Page3/data.csv')
    data['Date'] = pd.to_datetime(data['month_date'])
    data['Fiscal_Date'] = pd.to_datetime(data['month_fiscal']).dt.to_period('M')
    data['security_name'] = data['security_name'].astype('category')
    data['iso_country_symbol'] = data['iso_country_symbol'].astype('category')
    data['market_type'] = data['market_type'].astype('category')
    data['sedol'] = data['sedol'].astype('category')

    data = data[data['security_name'] != '3I Group']
    data['Year'] = data['Date'].dt.year
    securities_with_data = data.groupby('security_name')['Year'].nunique().reset_index()
    securities_with_data = securities_with_data[securities_with_data['Year'] >= 7]
    securities_with_data = securities_with_data['security_name'].tolist()

    data = data[data['security_name'].isin(securities_with_data)]
    data['country_exposure_pct'] = data['country_exposure(pct)']

    market_types = data['market_type'].unique()
    sectors = sorted(data['sector'].unique())
    default_sector = sectors[0]
    default_market_type = market_types[0]
    exposure_types = data['country_exposure_name'].unique()
    default_exposure_to = ['China', 'Hong Kong']

    default_securities = ['Nvidia (2379504)', 'Qualcomm (2714923)'] if any(mt == "developed market" for mt in market_types) else ['Apple', 'Amazon.Com']

    styles = {
        'container': {
            'margin': '20px auto',
            'width': '100%',
            'maxWidth': '1650px',
            'padding': '20px 40px',
            'fontFamily': 'Gill Sans',
        },
        'header': {
            'color': 'white',
            'padding': '30px',
            'marginBottom': '30px',
            'backgroundImage': 'url(/assets/right.jpg)',
            'backgroundBlendMode': 'darken',
            'height': '3vh',
            'backgroundSize': 'cover',
            'backgroundPosition': 'center',
            'marginTop': '-27px'
        },
        'filter_container': {
            'display': 'flex',
            'flexDirection': 'column',
            'backgroundColor': '#f2f2f2',
            'padding': '20px',
            'marginTop': '-15px',
            'gap': '20px'
        },
        'filters_row': {
            'display': 'flex',
            'gap': '20px',
            'alignItems': 'flex-start'
        },
        'filter_item': {
            'flex': '1',
            'padding': '0 10px'
        },
        'label': {
            'display': 'block',
            'marginBottom': '8px',
            'fontWeight': 'bold',
            'fontFamily': 'Gill Sans',
            'fontSize': '14px'
        },
        'dropdown': {
            'width': '100%',
            'fontFamily': 'Gill Sans',
            'fontSize': '14px',
            'minWidth': '150px'
        },
        'dropdown_companies': {
            'width': '100%',
            'fontFamily': 'Gill Sans',
            'fontSize': '14px',
            'flex': '2'
        },
        'chart_container': {
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '20px',
            'marginTop': '-38px'
        },
        'chart': {'className': 'chart-item'},
        'chart_two': {
            'className': 'chart-item',
            'marginTop': '-40px'
        },
        'graph': {
            'height': '550px',
            'max-width': '100%',
            'width': '100%',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'display': 'block'
        },
        'graph_two': {
            'height': '550px',
            'max-width': '100%',
            'width': '100%',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'margin-top': '20px',
            'display': 'block'
        }
    }

    layout = html.Div(style=styles['container'], children=[
        html.Div(style=styles['header'], children=[
            html.H1('Revenue Exposure Tool', style={
                'textShadow': '2px 2px 4px rgba(0, 0, 0.9, 0.9)',
                'fontFamily': 'Gill Sans',
                'fontWeight': 'bold',
                'fontSize': 'clamp(24px, 4vw, 50px)',
                'marginTop': '-12px'
            }),
        ]),

        html.Div(style=styles['filter_container'], children=[
            html.Div(style=styles['filters_row'], children=[
                # Market type filter
                html.Div(style=styles['filter_item'], children=[
                    html.Label('Select Market Type:', style=styles['label']),
                    dbc.Select(
                        id='market-type-dropdown',
                        options=[{'label': mt.title(), 'value': mt} for mt in market_types],
                        value=default_market_type,
                        style=styles['dropdown'],
                        class_name='mb-3'
                    )
                ]),

                # Country exposure filter
                html.Div(style=styles['filter_item'], children=[
                    html.Label('Select Countries:', style=styles['label']),
                    dbc.Select(
                        id='exposure-type-dropdown',
                        options=[{'label': et.title(), 'value': et} for et in exposure_types],
                        value=default_exposure_to,
                        multiple=True,
                        style=styles['dropdown'],
                        class_name='mb-3'
                    ),
                ]),

                # Sector filter
                html.Div(style=styles['filter_item'], children=[
                    html.Label('Select Sector:', style=styles['label']),
                    dbc.Select(
                        id='sector-dropdown',
                        options=[{'label': sector, 'value': sector} for sector in sectors],
                        value=default_sector,
                        style=styles['dropdown'],
                        class_name='mb-3'
                    )
                ]),

                # Securities filter
                html.Div(style={**styles['filter_item'], 'flex': '2'}, children=[
                    html.Label('Select Companies:', style=styles['label']),
                    dbc.Select(
                        id='securities-dropdown',
                        multiple=True,
                        value=default_securities,
                        style=styles['dropdown_companies'],
                        class_name='mb-3',
                        placeholder="You can select up to 3 companies"
                    ),
                ]),
            ]),

            # Download button
            html.Div(style={'display': 'flex', 'justifyContent': 'start', 'padding': '0 10px'}, children=[
                dbc.Button(
                    'Download Data',
                    id='download-csv-button',
                    color='primary',
                    className='me-2'
                ),
                dcc.Download(id='download-csv'),
            ]),
        ]),

        dbc.Tabs(id="tabs", active_tab='tab-1', children=[
            dbc.Tab(label='Exposure Charts', tab_id='tab-1', children=[
                html.Div(style={'marginTop': '20px'}, children=[
                    html.Div(style=styles['chart_container'], children=[
                        html.Div(style=styles['chart'], children=[
                            dcc.Graph(
                                id='country-exposure-revenue-graph',
                                config={
                                    'responsive': True,
                                    'autosizable': True,
                                    'displayModeBar': True,
                                    'displaylogo': False,
                                },
                                style=styles['graph']
                            )
                        ]),

                        # Source text
                        html.Div(style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'padding': '10px',
                        }, children=[
                            html.Div("Source: MSCI Economic Exposure Data", 
                                   style={'fontFamily': 'Gill Sans', 'fontSize': '17px', 'color': '#5a5a5a'}),
                            html.Div("SPG CSR | CMGW FRG | VRNC Quanthub", 
                                   style={'fontFamily': 'Gill Sans', 'fontSize': '17px', 'color': '#5a5a5a'}),
                        ]),

                        html.Div(style=styles['chart_two'], children=[
                            dcc.Graph(
                                id='country-exposure-pct-graph',
                                config={
                                    'responsive': True,
                                    'autosizable': True,
                                    'displayModeBar': True,
                                    'displaylogo': False,
                                },
                                style=styles['graph_two']
                            )
                        ]),

                        # Bottom source text
                        html.Div(style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'padding': '10px',
                        }, children=[
                            html.Div("Source: MSCI Economic Exposure Data", 
                                   style={'fontFamily': 'Gill Sans', 'fontSize': '18px', 'color': '#5a5a5a'}),
                            html.Div("SPG CSR, CMGW FRG, VRNC Quanthub", 
                                   style={'fontFamily': 'Gill Sans', 'fontSize': '18px', 'color': '#5a5a5a'}),
                        ]),
                    ])
                ]),
            ]),

            dbc.Tab(label='Top Companies by Market Cap', tab_id='tab-2', children=[
                html.Div(style={
                    'padding': '20px',
                    'backgroundColor': '#ffffff',
                    'borderRadius': '5px',
                    'border': '1px solid #dee2e6',
                    'marginTop': '20px'
                }, children=[
                    dash_table.DataTable(
                        id='datatable',
                        columns=[{'name': col, 'id': col} for col in df.columns],
                        data=df.to_dict('records'),
                        style_table={
                            'overflowX': 'auto',
                            'maxWidth': '1500px',
                            'margin': '0 auto'
                        },
                        style_header={
                            'backgroundColor': '#145DA0',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            'padding': '12px',
                            'fontFamily': 'Gill Sans',
                            'fontSize': '15px'
                        },
                        style_cell={
                            'padding': '12px',
                            'textAlign': 'left',
                            'backgroundColor': 'white',
                            'color': '#2c3e50',
                            'fontSize': '14px',
                            'fontFamily': 'Gill Sans'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f9f9f9'
                            }
                        ],
                        page_size=50,
                    )
                ])
            ]),
        ]),

        dbc.Alert(
            id='security-alert',
            is_open=False,
            duration=4000,
            color='warning',
            dismissable=True,
            style={'margin-top': '10px'}
        )
    ])

    return layout