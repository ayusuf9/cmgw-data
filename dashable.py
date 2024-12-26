import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os

ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
PLOTLY_LOGO = "/assets/logo.svg"

nav_items = [
    dbc.NavItem(dbc.NavLink("HOME", href="/", className="text-light")),
    dbc.NavItem(dbc.NavLink("ABOUT", href="/page1", className="text-light")),
    dbc.NavItem(dbc.NavLink("COMPARISON", href="/page2", className="text-light")),
]

flags = dbc.Row(
    [
        dbc.Col(html.Img(src="/assets/cn.svg", height="20px", className="rounded"), className="ms-2"),
        dbc.Col(html.Div("|", style={"color": "#808080"}, className="mx-2")),
        dbc.Col(html.Img(src="/assets/hk.svg", height="20px", className="rounded")),
        dbc.Col(html.Div("|", style={"color": "#808080"}, className="mx-2")),
        dbc.Col(html.Img(src="/assets/tw.svg", height="20px", className="rounded")),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Left side - Logo and brand
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                    dbc.Col(dbc.NavbarBrand("Exposure Tool", className="ms-2")),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                        className="ps-5 ms-5 large-shift"
                    ),
                ],
                className="me-auto",
            ),
            # Center - Navigation items
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Nav(
                            nav_items,
                            navbar=True,
                            className="justify-content-center"
                        ),
                        className="flex-grow-1 text-center",
                    ),
                ],
                className="flex-grow-1 justify-content-center",
            ),
            # Right side - Flags
            dbc.Row(
                [
                    dbc.Col(
                        flags,
                        className="pe-5 me-5 large-shift",
                    ),
                ],
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    style={
        "fontFamily": "AvenirNextRegular, Arial, Helvetica, sans-serif"
    },
)

def get_data():
    data = pd.read_csv('pages/Page3/new_exp_data.csv')
    return data

def get_defaults():
    data = get_data()
    market_types = data['market_type'].unique()
    default_market_type = market_types[1]
    default_securities = data[data['market_type'] == default_market_type]['security_name'].unique()[-2:]
    return default_market_type, default_securities

def get_page3(app):
    # Your existing data loading code remains the same
    dfa = pd.read_csv('pages/Page3/updated_ch_hk_data.csv')
    df = dfa[['companyname', 'sector', 'total_revenue', 'china_plus_hk_rev', 'china_plus_hk_pct']]
    df.columns = ['Company Name', 'Sector', 'Total Revenue', 'CH, HK Revenue', 'CH, HK Percentage']

    # Rest of your data processing code remains the same
    data = pd.read_csv('pages/Page3/new_exp_data.csv')
    # ... (rest of the data processing)

    styles = {
        'container': {
            'margin': '0 auto',  # Modified to remove top margin due to navbar
            'width': '100%',
            'maxWidth': '1650px',
            'padding': '20px 40px',
            'fontFamily': 'Gill Sans',
        },
        # Remove the header style since we're not using it anymore
        'filter_container': {
            'display': 'flex',
            'flexDirection': 'row', 
            'backgroundColor': '#f2f2f2',
            'padding': '20px',
            'marginTop': '0px',  # Modified to work with navbar
            'gap': '10px',
            'alignItems': 'flex-start'
        },
        # ... rest of your styles remain the same
    }

    layout = html.Div(style=styles['container'], children=[
        navbar,  # Add the navbar here
        html.Div(style=styles['filter_container'], children=[
            # ... rest of your layout remains the same
        ]),
        # ... rest of your components
    ])

    return layout