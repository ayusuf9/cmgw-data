import dash_bootstrap_components as dbc
from dash import html

styles = {
    'container': {
        'padding': '40px',
        'max-width': '1400px',
        'margin': '0 auto',
        'font-family': "'DM Sans', sans-serif",
        'display': 'flex',
        'gap': '40px'
    },
    'main_content': {
        'flex': '1',
        'max-width': '900px'
    },
    'team_sidebar': {
        'width': '300px',
        'padding': '20px',
        'background': 'white',
        'border-radius': '8px',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
    },
    'team_member': {
        'display': 'flex',
        'align-items': 'center',
        'margin-bottom': '15px',
        'padding': '10px',
        'border-radius': '8px',
        'transition': 'background-color 0.3s'
    },
    'team_member_img': {
        'width': '40px',
        'height': '40px',
        'border-radius': '50%',
        'margin-right': '15px'
    },
    'team_member_info': {
        'flex': '1'
    },
    'section': {
        'margin-bottom': '30px'
    },
    'subsection': {
        'margin-left': '20px',
        'margin-bottom': '15px'
    }
}

# Team members data
team_members = [
    {"name": "Anne Vandenabeele", "role": "ABV", "img": "/assets/profile-placeholder.png"},
    {"name": "Dana Mott", "role": "DACM", "img": "/assets/profile-placeholder.png"},
    {"name": "Darrell Spence", "role": "DTS", "img": "/assets/profile-placeholder.png"},
    {"name": "Elizabeth Mooney", "role": "EAFM", "img": "/assets/profile-placeholder.png"},
    {"name": "Jared Franz", "role": "JASF", "img": "/assets/profile-placeholder.png"},
    {"name": "Tina Chen", "role": "TNAC", "img": "/assets/profile-placeholder.png"}
]

tab_layout = html.Div(style=styles['container'], children=[
    # Main Content
    html.Div(style=styles['main_content'], children=[
        html.H1("Exposure Tool", style={'margin-bottom': '20px', 'color': '#2c3e50'}),
        
        html.P([
            "CSR Exposure is a tool that aggregates the models and views published by CSR analysts. ",
            "Its purpose is to easily allow users to compare and contrast CSR analyst views on portfolios, sectors, and companies ",
            "to make informed investment decisions."
        ], style={'margin-bottom': '30px', 'line-height': '1.6', 'color': '#5a6c7d'}),

        html.Div(style=styles['section'], children=[
            html.P("The CSR Analyst models we currently have included into Exposure are:", 
                  style={'margin-bottom': '20px', 'font-weight': '500'}),
            
            # ABV's TOPIX Model
            html.Div(style=styles['section'], children=[
                html.H3("ABV's TOPIX Model:", style={'color': '#2c3e50', 'margin-bottom': '10px', 'font-size': '1.1rem'}),
                html.P([
                    "A model that shows how company performance may be sensitive to or vary against different global macroeconomic indicators, ",
                    "highlighting which companies or industries have historically outperformed during different phases of the cycle using hit rates. ",
                    "It offers a way to identify and incorporate macroeconomic data into individual company, sectors, and to view these factors ",
                    "within individual portfolio. For now, this work is only available for equities and against the U.S. cycles and those listed below. ",
                    "We are working on broadening out to different benchmarks, countries, and cycles."
                ], style={'margin-bottom': '15px', 'line-height': '1.6', 'color': '#5a6c7d'}),
                
                html.P("Japanese Macroeconomic cycles include:", 
                      style={'margin-bottom': '10px', 'font-weight': '500'}),
                html.Ul([
                    html.Li("Japan Overall activity cycle"),
                    html.Li("Japan Manufacturing cycle"),
                    html.Li("Japan Employment cycle"),
                    html.Li("Japan Inflation (CPI all items) cycle"),
                    html.Li("Japan Oil cycle"),
                    html.Li("Japan Monetary conditions cycle"),
                    html.Li("Japan JGB curve (30 year less policy rate) cycle"),
                    html.Li("Japan 10-yr JGB yield cycle"),
                    html.Li("Japan JPY/USD, %YoY cycle"),
                    html.Li("Japan External demand cycle"),
                ], style={'margin-left': '40px', 'line-height': '1.6', 'color': '#5a6c7d'})
            ]),

            # DACM's Star Power Rating
            html.Div(style=styles['section'], children=[
                html.H3("DACM's Star Power Rating:", style={'color': '#2c3e50', 'margin-bottom': '10px', 'font-size': '1.1rem'}),
                html.P([
                    "The Star Power Rating (SPR) is a metric created by DACM through a project on disruption that was a collaboration with ACM, BYC, CXXS, CHG, DDO, JWK, KMBZ, LXN, and NNC. ",
                    "SPR metrics are on a scale of 0% (worst) to 100% (best). The intention is for the metric to help investors identify high-quality companies with the potential to be disruptive and generate high returns."
                ], style={'margin-bottom': '15px', 'line-height': '1.6', 'color': '#5a6c7d'})
            ]),

            # DTS's Headwind/Tailwind Framework
            html.Div(style=styles['section'], children=[
                html.H3("DTS's Headwind/Tailwind Framework:", style={'color': '#2c3e50', 'margin-bottom': '10px', 'font-size': '1.1rem'}),
                html.P([
                    "A framework developed over the years that highlight where macroeconomic, political, and other factors may impact specific companies or industries. ",
                    "This framework is continuously evolving, as such, companies and industries may be added and removed over time. ",
                    "This framework is entirely from a macroeconomic perspective. There are many factors that play a role in determining the return of a company or industry, ",
                    "and this is not intended to be a substitute for the bottom-up analysis that is done on these companies and industries. ",
                    "Rather, it is meant to provide a different perspective that can hopefully complement that analysis."
                ], style={'margin-bottom': '15px', 'line-height': '1.6', 'color': '#5a6c7d'})
            ]),

            # JASF's Macro Cycle Tool
            html.Div(style=styles['section'], children=[
                html.H3("JASF's Macro Cycle Tool:", style={'color': '#2c3e50', 'margin-bottom': '10px', 'font-size': '1.1rem'}),
                html.P([
                    "A model that shows how company performance may be sensitive to or vary against different U.S. macroeconomic indicators, ",
                    "highlighting which companies or industries have historically outperformed during different phases of the cycle using hit rates. ",
                    "It offers a way to identify and incorporate macroeconomic data into individual company, sectors, and to view these factors within individual portfolio."
                ], style={'margin-bottom': '15px', 'line-height': '1.6', 'color': '#5a6c7d'})
            ])
        ])
    ]),

    # Team Sidebar
    html.Div(style=styles['team_sidebar'], children=[
        html.H2("CSR Team", style={'margin-bottom': '20px', 'color': '#2c3e50'}),
        html.Div([
            html.Div(style=styles['team_member'], children=[
                html.Img(src=member["img"], style=styles['team_member_img']),
                html.Div(style=styles['team_member_info'], children=[
                    html.Div(member["name"], style={'font-weight': '500'}),
                    html.Div(member["role"], style={'color': '#6c757d', 'font-size': '0.9rem'})
                ])
            ]) for member in team_members
        ])
    ])
])