import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Read and prepare the data
df = pd.read_csv("updated_data.csv")
df['securities'] = df['security_name'].astype(str) + ' (' + df['sedol'].astype(str) + ')'
df['month_date'] = pd.to_datetime(df['month_date'])
df['Year'] = df['month_date'].dt.year

# Color palette
cg_color_pallet = {
    'sapphire': '#005F9E',
    'ocean': '#009CDC',
    'turquoise': '#00AEA9',
}
colors_to_use = [cg_color_pallet['sapphire'], cg_color_pallet['ocean'], cg_color_pallet['turquoise']]

# App layout
app.layout = html.Div([
    html.H1("Security Exposure Analysis Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown container
    html.Div([
        html.Div([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['country_exposure_name'].unique())],
                value=df['country_exposure_name'].iloc[0]
            )
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Select Sector:"),
            dcc.Dropdown(id='sector-dropdown')
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Select First Security:"),
            dcc.Dropdown(id='security1-dropdown')
        ], style={'width': '24%', 'display': 'inline-block', 'marginRight': '1%'}),
        
        html.Div([
            html.Label("Select Second Security:"),
            dcc.Dropdown(id='security2-dropdown')
        ], style={'width': '24%', 'display': 'inline-block'}),
    ], style={'padding': '20px'}),
    
    # Graphs container
    html.Div([
        html.Div([
            dcc.Graph(id='bubble-chart1')
        ], style={'width': '49%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='bubble-chart2')
        ], style={'width': '49%', 'display': 'inline-block'})
    ])
])

# Callbacks for linked dropdowns
@app.callback(
    Output('sector-dropdown', 'options'),
    Output('sector-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def update_sector_dropdown(selected_country):
    filtered_df = df[df['country_exposure_name'] == selected_country]
    sectors = sorted(filtered_df['sector'].unique())
    return [{'label': i, 'value': i} for i in sectors], sectors[0] if sectors else None

@app.callback(
    [Output('security1-dropdown', 'options'),
     Output('security1-dropdown', 'value'),
     Output('security2-dropdown', 'options'),
     Output('security2-dropdown', 'value')],
    [Input('country-dropdown', 'value'),
     Input('sector-dropdown', 'value')]
)
def update_security_dropdowns(selected_country, selected_sector):
    filtered_df = df[
        (df['country_exposure_name'] == selected_country) &
        (df['sector'] == selected_sector)
    ]
    securities = sorted(filtered_df['securities'].unique())
    options = [{'label': i, 'value': i} for i in securities]
    
    # Set default values to first two securities if available
    default_value1 = securities[0] if len(securities) > 0 else None
    default_value2 = securities[1] if len(securities) > 1 else default_value1
    
    return options, default_value1, options, default_value2

# Callback for updating charts
@app.callback(
    [Output('bubble-chart1', 'figure'),
     Output('bubble-chart2', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('security1-dropdown', 'value'),
     Input('security2-dropdown', 'value')]
)
def update_charts(country, security1, security2):
    def create_bubble_chart(security, color):
        filtered_df = df[
            (df['country_exposure_name'] == country) &
            (df['securities'] == security)
        ]
        
        latest_obs = filtered_df.loc[
            filtered_df.groupby(['securities', filtered_df['month_date'].dt.year])['month_date'].idxmax()
        ]
        
        fig = px.scatter(
            latest_obs,
            x='Year',
            y='country_exposure_revenue',
            size='country_exposure(pct)',
            color='securities',
            hover_name="securities",
            size_max=30,
            template='plotly_white',
            color_discrete_sequence=[color]
        )
        
        fig.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>" +
                "Year: %{x}<br>" +
                "Revenue: $%{y:,.0f}<br>" +
                "Exposure: %{marker.size:.2f}%<br><extra></extra>"
            )
        )
        
        fig.update_xaxes(
            linecolor='grey',
            linewidth=3.4,
            mirror='ticks',
            title="",
            showgrid=False
        )
        
        fig.update_yaxes(
            title="",
            anchor='x',
            autorange=True,
            gridcolor='lightgray',
        )
        
        fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(family="'DM Sans', sans-serif", size=14),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="'DM Sans', sans-serif",
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11),
                itemsizing='constant'
            )
        )
        
        fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[-1]))
        return fig
    
    fig1 = create_bubble_chart(security1, cg_color_pallet['sapphire'])
    fig2 = create_bubble_chart(security2, cg_color_pallet['ocean'])
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)