import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc

def get_data():
  #data = pd.read_csv('pages/Page3/data.csv')
  data = pd.read_csv('pages/Page3/updated_data.csv')
  return data

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

  default_market_type = market_types[0]
  market_types_list = list(data['market_type'].unique())

  #-------------------EXPOSURE--------------------------#
  exposure_types = data['country_exposure_name'].unique()

  default_exposure_to = ['China', 'Hong Kong']  # Set default selected countries
  exposure_types_list = list(data['country_exposure_name'].unique())

  if any(market_type == "developed market" for market_type in market_types_list):
      default_securities = ['Nvidia (2379504)', 'Qualcomm (2714923)']
  else:
      default_securities = ['Apple', 'Amazon.Com']

  # default_securities = data[data['market_type'] == default_market_type]['security_name'].unique()[-2:]

  styles = {
      'container': {
          'margin': '20px auto',
          'width': '100%',
          'maxWidth': '1650px',
          'padding': '20px 40px',
          'fontFamily': 'Gill Sans',
          #'transform': 'scale(1.2)'
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
          'flexWrap': 'wrap',
          'gap': '10px', 
          'marginBottom': '10px',
          'backgroundColor': '#f2f2f2',
          'padding': '10px', 
          'marginTop': '-15px',
          'height': '120px'
      },
      'filter_item': {
          'flex': '1 1 300px',
          'minWidth': '0',
          'maxWidth': '100%'
      },
      'label': {
          'marginBottom': '5px',
          'marginTop': '5px',
          'fontWeight': 'bold',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px'
      },
      'label_country': {
          'marginBottom': '5px',
          'marginTop': '5px',
          'fontWeight': 'bold',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px',
          'marginLeft': '-280px'
      },
      'label_two': {
          'marginBottom': '5px',
          'marginTop': '5px',
          'fontWeight': 'bold',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px',
          'marginLeft': '-280px'
      },
      'dropdown': {
          'width': '200px',
          'maxWidth': '100%',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px'
      },

      'dropdown_one': {
          'width': '300px',
          'maxWidth': '100%',
          'marginLeft': '-138px',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px'
      },

      'dropdown_two': {
          'width': '1300px',
          'maxWidth': '100%',
          'marginLeft': '-225px',
          'fontFamily': 'Gill Sans',
          'fontSize': '14px'
      },

      'chart_container': {
          'display': 'flex',
          'flexDirection': 'column',
          'gap': '20px',
          'marginTop': '-38px'
      },
            
      'chart': {
          'className': 'chart-item'
      },

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
          'height': '550px',  # Fixed height instead of viewport-based
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
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '20px'
        }, children=[

            # The market type filter
            html.Div(style=styles['filter_item'], children=[
                html.Label('Select Market Type:', style=styles['label']),
                dcc.Dropdown(
                    id='market-type-dropdown',
                    options=[
                        {'label': market_type.title(), 'value': market_type}
                        for market_type in market_types
                    ],
                    value=default_market_type,
                    style=styles['dropdown'],
                    clearable=False,
                    optionHeight=50
                )
            ]),

            # The country exposure type filter
            html.Div(
                style=styles['filter_item'],
                children=[
                    html.Label('Select Countries:', style=styles['label_country']),
                    dcc.Dropdown(
                        id='exposure-type-dropdown',
                        options=[
                            {'label': exposure_type.title(), 'value': exposure_type}
                            for exposure_type in exposure_types
                        ],
                        value=default_exposure_to,
                        multi=True,  # Enable multi-select functionality
                        style=styles['dropdown_one'],
                        clearable=False,
                        optionHeight=50,
                    ),
                ],
            ),

            # The sector filter
            html.Div(style=styles['filter_item'], children=[
                html.Label('Select Sectors:', style=styles['label_country']),
                dcc.Dropdown(
                    id='sector-dropdown',
                    multi=True,
                    style=styles['dropdown_one'],
                    clearable=False,
                    optionHeight=50,
                    placeholder="Select sectors"
                ),
            ]),

            # The company selection filter
            html.Div(style=styles['filter_item'], children=[
                html.Label('Select Companies:', style=styles['label_two']),
                dcc.Dropdown(
                    id='securities-dropdown',
                    multi=True,
                    value=default_securities,
                    style=styles['dropdown_two'],
                    clearable=False,
                    placeholder="You can select up to 3 companies",
                ),
            ]),
        ]),  # End of first Div in filter_container

        # Updated Div with new button
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'marginLeft': '-10px',
                'marginTop': '30px'
            },
            children=[
                html.Button(
                    'Download Data',
                    id='download-csv-button',
                    n_clicks=0,
                    style={
                        'fontSize': '16px',
                        'fontFamily': 'Avenir Next LT Com, sans-serif',
                        'cursor': 'pointer',
                        'backgroundColor': '#1591ea',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '5px',
                        'transition': 'background-color 0.3s',
                        'width': '150px',
                        'height': '40px',
                        'marginRight': '10px',  # Space between buttons
                    }
                ),
                dcc.Download(id='download-csv'),
            ]
        ),
    ]),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Exposure Charts', value='tab-1', children=[
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
                            className='dash-graph-wide',
                            style=styles['graph']
                        )
                    ]),

                    # Text between graphs
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'padding': '10px',
                        'borderRadius': '5px',
                    }, children=[
                        html.Div("Source: MSCI Economic Exposure Data", style={
                            'width': '45%',
                            'marginLeft': '60px',
                            'textAlign': 'left',
                            'fontFamily': 'Gill Sans',
                            'fontSize': '17px',
                            'marginTop': '-20px',
                            'color': '#5a5a5a'
                        }),
                        html.Div("SPG CSR | CMGW FRG | VRNC Quanthub", style={
                            'width': '45%',
                            'marginRight': '60px',
                            'textAlign': 'right',
                            'fontFamily': 'Gill Sans',
                            'fontSize': '17px',
                            'marginTop': '-20px',
                            'color': '#5a5a5a'
                        }),
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
                            className='dash-graph-wide',
                            style=styles['graph_two']
                        )
                    ]),

                    # Bottom text
                    html.Div(style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'padding': '10px',
                        'borderRadius': '5px',
                    }, children=[
                        html.Div("Source: MSCI Economic Exposure Data", style={
                            'width': '45%',
                            'marginLeft': '60px',
                            'textAlign': 'left',
                            'fontFamily': 'Gill Sans',
                            'fontSize': '18px',
                            'marginTop': '-20px',
                            'color': '#5a5a5a'
                        }),
                        html.Div("SPG CSR, CMGW FRG, VRNC Quanthub", style={
                            'width': '45%',
                            'marginRight': '60px',
                            'textAlign': 'right',
                            'fontFamily': 'Gill Sans',
                            'fontSize': '18px',
                            'marginTop': '-20px',
                            'color': '#5a5a5a'
                        }),
                    ]),
                ])
            ]),
        ]),
    
      dcc.Tab(label='Top Companies by Market Cap', value='tab-2', children=[
            html.Div(style={
                'padding': '20px',
                'backgroundColor': '#ffffff',
                'borderRadius': '0 0 5px 5px',
                'border': '1px solid #dee2e6',
                'borderTop': 'none'
            }, children=[
                html.Div([
                    dash_table.DataTable(
                        id='datatable',
                        columns=[{'name': col, 'id': col} for col in df.columns],
                        data=df.to_dict('records'),
                      
                        style_table={
                            'overflowX': 'auto',
                            'maxWidth': '1500px',
                            'maxHeight': '1200px',
                            'margin': '20px auto 0 auto'
                        },
                        style_header={
                            'backgroundColor':'#145DA0',
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
                            },
                            {
                                'if': {'state': 'selected'},
                                'backgroundColor': '#e6f3ff',
                                'border': '1px solid #1591ea' 
                            }
                        ],
                        page_action='native',
                        page_size=50,
                    )
                ], style={'margin': '20px'}),
              
                html.Div(id='selection-info', 
                        style={
                            'margin': '20px',
                            'textAlign': 'center',
                            'color': '#2c3e50',
                            'fontFamily': 'Gill Sans'
                        })
            ])
        ]),
    ],

 #], 
  style={
      'fontFamily': 'Gill Sans',
      'marginTop': '20px'
  }),

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