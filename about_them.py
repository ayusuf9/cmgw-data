import dash_bootstrap_components as dbc
from dash import html

# Define some custom styles
styles = {
    'container': {
        'padding': '40px',
        'max-width': '1200px',
        'margin': '0 auto',
        'font-family': "'DM Sans', sans-serif",
    },
    'header': {
        'text-align': 'center',
        'margin-bottom': '40px',
        'padding': '20px',
        'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
        'border-radius': '10px',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
    'section': {
        'margin-bottom': '30px',
        'padding': '25px',
        'background-color': 'white',
        'border-radius': '8px',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
    },
    'feature_card': {
        'height': '100%',
        'border': 'none',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
        'transition': 'transform 0.3s ease',
    },
}

# Create the about page layout
tab_layout = html.Div(style=styles['container'], children=[
    # Header Section
    html.Div(style=styles['header'], children=[
        html.H1("About the Exposure Tool", 
                style={'color': '#2c3e50', 'font-weight': '700', 'margin-bottom': '20px'}),
        html.P("A comprehensive solution for analyzing economic exposure across global markets",
               style={'color': '#5a6c7d', 'font-size': '1.2rem'}),
    ]),

    # Main Content Sections
    html.Div(style=styles['section'], children=[
        html.H2("Overview", style={'color': '#2c3e50', 'margin-bottom': '20px'}),
        html.P([
            "The Exposure Tool is a sophisticated platform designed to help investors and analysts understand ",
            "companies' economic exposure to different markets, with a particular focus on China and Hong Kong. ",
            "By leveraging MSCI's economic exposure data, we provide detailed insights into revenue sources ",
            "and market dependencies across various sectors and companies."
        ], style={'line-height': '1.6', 'color': '#5a6c7d'}),
    ]),

    # Features Section
    html.Div(style=styles['section'], children=[
        html.H2("Key Features", style={'color': '#2c3e50', 'margin-bottom': '30px'}),
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Div(html.I(className="fas fa-chart-line fa-2x", style={'color': '#3498db'}),
                         style={'text-align': 'center', 'margin': '20px 0'}),
                dbc.CardBody([
                    html.H4("Revenue Analysis", className="card-title", style={'text-align': 'center'}),
                    html.P("Track revenue exposure across different markets with interactive visualizations",
                          className="card-text", style={'text-align': 'center'})
                ])
            ], style=styles['feature_card']), width=4, className="mb-4"),

            dbc.Col(dbc.Card([
                html.Div(html.I(className="fas fa-globe fa-2x", style={'color': '#2ecc71'}),
                         style={'text-align': 'center', 'margin': '20px 0'}),
                dbc.CardBody([
                    html.H4("Market Insights", className="card-title", style={'text-align': 'center'}),
                    html.P("Compare exposure percentages across different geographical regions",
                          className="card-text", style={'text-align': 'center'})
                ])
            ], style=styles['feature_card']), width=4, className="mb-4"),

            dbc.Col(dbc.Card([
                html.Div(html.I(className="fas fa-industry fa-2x", style={'color': '#e74c3c'}),
                         style={'text-align': 'center', 'margin': '20px 0'}),
                dbc.CardBody([
                    html.H4("Sector Analysis", className="card-title", style={'text-align': 'center'}),
                    html.P("Analyze exposure patterns across different industry sectors",
                          className="card-text", style={'text-align': 'center'})
                ])
            ], style=styles['feature_card']), width=4, className="mb-4"),
        ], className="mb-4"),
    ]),

    # Data Sources Section
    html.Div(style=styles['section'], children=[
        html.H2("Data Sources", style={'color': '#2c3e50', 'margin-bottom': '20px'}),
        html.P([
            "Our tool utilizes high-quality data from trusted sources:",
            html.Ul([
                html.Li("MSCI Economic Exposure Data", style={'margin': '10px 0'}),
                html.Li("Company Financial Reports", style={'margin': '10px 0'}),
                html.Li("Market Analysis Reports", style={'margin': '10px 0'}),
            ], style={'list-style-type': 'none', 'padding-left': '20px'})
        ], style={'line-height': '1.6', 'color': '#5a6c7d'}),
    ]),

    # Footer Section
    html.Div(style={'text-align': 'center', 'margin-top': '40px', 'padding': '20px',
                    'border-top': '1px solid #eee'}, children=[
        html.P([
            "Developed by SPG CSR | CMGW FRG | VRNC Quanthub",
            html.Br(),
            "© 2024 All Rights Reserved"
        ], style={'color': '#8395a7', 'font-size': '0.9rem'})
    ])
])