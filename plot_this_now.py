import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Custom plotting components
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

# Helper function from original code
def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and prepare the data
df = pd.read_csv('updated_data.csv')
df['month_date'] = pd.to_datetime(df['month_date'])
available_securities = sorted(df['security_name'].unique())

# Define the layout
app.layout = html.Div([
    html.H1("Revenue Exposure Analysis Dashboard", 
            style={'textAlign': 'center', 'marginBottom': 30, 'color': cg_color_pallet['dark_sapphire'],
                   'fontFamily': 'Arial', 'fontSize': 26}),
    
    html.Div([
        html.Label('Select Securities:', style={'fontFamily': 'Arial Black', 'color': 'grey'}),
        dcc.Dropdown(
            id='security-selector',
            options=[{'label': sec, 'value': sec} for sec in available_securities],
            value=[available_securities[0]],
            multi=True
        )
    ], style={'width': '50%', 'margin': 'auto', 'marginBottom': 30}),
    
    dcc.Graph(id='revenue-exposure-graph')
])

@app.callback(
    Output('revenue-exposure-graph', 'figure'),
    [Input('security-selector', 'value')]
)
def update_graph(selected_securities):
    if not selected_securities:
        return go.Figure()
    
    # Create the base plot configuration
    revenue_exposure_config = {
        'data_fn': lambda: df.query('country_exposure_name.str.lower() == "china" and security_name == @selected_securities[0]')
        .set_index('month_date')[['country_exposure_revenue']],
        'types': ['line'],
        'series_config': [
            {
                'line': {'width': 5, 'color': cg_color_pallet['dark_sapphire']},
                'showlegend': True,
                'hoverlabel': {"namelength": -1},
                'hovertemplate': "(%{text}) %{y}",
                'hoverinfo': 'text+y'
            }
        ],
        'yaxes_primary': {
            'mirror': True,
        },
        'annotations': {
            'title': "Country Revenue Exposure Over Time",
            'y1_label': "Revenue ($)",
            'y2_label': "Revenue ($)",
            'source': "MSCI Economic Exposure Data",
            'author': "SPG | CMGW | VRNC"
        },
        'precision': 0,
        'yrange': [[0, None]],
        'autorange': True,
        'endpoint_yshift': [-10, 10],
        'isRangeSelector': True
    }

    # Initialize plot classes from the custom module
    plot_instance = Plot(revenue_exposure_config)
    fig = plot_instance.get_fig(isRangeSelector=True)

    # Add annotations
    annotations = Annotations(
        annotations_config=default_annotations_original,
        chart_config=revenue_exposure_config,
        df=plot_instance.df
    ).get_annotations()

    # Update layout with custom settings
    fig.update_layout(
        height=800,
        hovermode="x unified",
        plot_bgcolor='white',
        legend={
            'x': 0.02,
            'y': 1.06,
            'orientation': 'h',
            'xanchor': 'left',
            'borderwidth': 0,
            'font': {'family': "Arial Black", 'size': 12, 'color': 'grey'},
            'bgcolor': 'rgba(0,0,0,0)'
        },
        annotations=annotations,
        margin=go.layout.Margin(l=10, r=10, b=100, t=100, pad=10)
    )

    # Add additional traces for other selected securities
    for security in selected_securities[1:]:
        security_data = df.query('country_exposure_name.str.lower() == "china" and security_name == @security') \
            .set_index('month_date')[['country_exposure_revenue']]
        
        fig.add_trace(
            go.Scatter(
                x=security_data.index,
                y=security_data['country_exposure_revenue'],
                name=security,
                mode='lines',
                line={'width': 2},
                showlegend=True,
                hoverlabel={"namelength": -1},
                hovertemplate="(%{text}) %{y}",
                text=[security] * len(security_data)
            )
        )

    return fig

class Plot:
    def __init__(self, chart_config):
        self.chart_config = chart_config
        self.df = chart_config['data_fn']()
        self.fig = self._create_fig()
    
    def _create_fig(self):
        return make_subplots(specs=[[{"secondary_y": True}]])
    
    def get_fig(self, isRangeSelector=False):
        self.fig = self._add_traces()
        if isRangeSelector:
            self.fig = self._add_rangeselector()
        return self.fig
    
    def _add_traces(self):
        for c, series in enumerate(self.df.columns):
            self.fig.add_trace(
                go.Scatter(
                    x=self.df.index,
                    y=self.df[series],
                    text=[i.strftime("%b %Y") for i in self.df.index],
                    mode='lines',
                    name=series,
                    **self.chart_config['series_config'][c]
                )
            )
        return self.fig
    
    def _add_rangeselector(self):
        currDate = self.df.index[-1]
        config = self.chart_config.get('range_selector_config', {
            '1YR': {'delta': timedelta(days=365), 'padding': timedelta(days=30)},
            '5YR': {'delta': timedelta(days=365*5), 'padding': timedelta(days=30*5)},
            '10YR': {'delta': timedelta(days=365*10), 'padding': timedelta(days=30*10)},
            'Max': {'delta': None, 'padding': timedelta(days=30)}
        })
        
        buttons = []
        for label, delta_dict in config.items():
            try:
                delta = delta_dict['delta'] if delta_dict['delta'] else self.df.index[0]
                new_domain = [currDate-delta, currDate + delta_dict['padding']]
                buttons.append({
                    'label': label,
                    'method': "update",
                    'args': [{}, {'xaxis': {'range': new_domain}}]
                })
            except Exception as e:
                print(f"Error (_add_rangeselector): {e}")
        
        self.fig.update_layout(
            updatemenus=[
                go.layout.Updatemenu(
                    buttons=buttons,
                    type="buttons",
                    x=0,
                    xanchor="left",
                    y=1.18,
                    yanchor="top",
                    direction='right'
                )
            ]
        )
        return self.fig

class Annotations:
    def __init__(self, annotations_config, chart_config, df):
        self.df = df
        self.chart_config_annotations = chart_config.get('annotations', {})
        self.annotations_config = self._update_default_config(annotations_config)
    
    def _update_default_config(self, annotations_config):
        asOf = str(self.df.index[-1]).split(' ')[0]
        default_text_config = {
            'source': self.chart_config_annotations.get('source', ''),
            'author': self.chart_config_annotations.get('author', ''),
            'title': f"<b>{self.chart_config_annotations.get('title', '')}</b>",
            'as_of_date': f"<b>Data as of: {asOf}</b>",
            'y_primary': self.chart_config_annotations.get('y1_label', ''),
            'y_secondary': self.chart_config_annotations.get('y2_label', '')
        }
        
        for key, value in default_text_config.items():
            if key in annotations_config:
                annotations_config[key]['text'] = value
        
        return annotations_config
    
    def get_annotations(self):
        return [self._get_config(config) for key, config in self.annotations_config.items() 
                if config.get('text', False)]
    
    def _get_config(self, config):
        return {
            'xref': config.get('xref', 'paper'),
            'yref': config.get('yref', 'paper'),
            'x': config.get('x', self.df.index[-1]),
            'y': config.get('y', 0),
            'xanchor': config.get('xanchor', 'left'),
            'yanchor': config.get('yanchor', 'top'),
            'text': config.get('text', ''),
            'font': config.get('font', {'family': 'Arial', 'size': 12, 'color': 'grey'}),
            'showarrow': config.get('showarrow', False)
        }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)