from flask.helpers import get_root_path
import dash
from dash import Dash, html
import logging
import dash_bootstrap_components as dbc
import os
from constants import log_key
from page.PageCallbacks import register_page3_callbacks
from page.PageDash import get_page3

logger = logging.getLogger(log_key)

class Callbacks:
  def __init__(self):
      self.default_app = None
      self.apps = dict()

  def apply_custom_index_string(self, app):
      app.index_string = '''
      <!DOCTYPE html>
      <html>
      <head>
          {%metas%}
          <title>{%title%}</title>
          {%favicon%}
          {%css%}
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>

          .chart_container: {
              display: flex;
              flexWrap: wrap;
              gap: 10px;
          }

          .chart-item {
              flex: 1 1 calc(50% - 10px);
              minWidth: 300px;
              width: 100%;
          }

          .dash-graph-wide {
              height: 60vh;
              width: 100%;
          }

          @media (min-width: 2000px) {
              .dash-graph-wide {
                  height: 30vh;
              }
          }
          </style> 
      </head>
      <body>
          {%app_entry%}
          <footer>
              {%config%}
              {%scripts%}
              {%renderer%}
          </footer>
      </body>
      </html>
      '''

  def create_app(self, id, page_title, external_stylesheets=None):
      self.apps[id] = Dash(
          name=page_title,
          requests_pathname_prefix=f"/{id}/",
          title=page_title,
          external_stylesheets=external_stylesheets,
      )

  def init_page3(self):
      key = "page3"
      self.create_app(key, "Exposure Tool")
      app = self.apps["page3"]
      self.apps[key].layout = get_page3(app)
      self.apply_custom_index_string(app)
      register_page3_callbacks(app)

  def register_callbacks(self):
      self.default_app = Dash(
          name='Exposure Tool',
          requests_pathname_prefix='/',
          title="Exposure Tool",
      )
      self.init_page3()
      # Set the default app's layout to be the same as page3
      self.default_app.layout = get_page3(self.default_app)
      self.apply_custom_index_string(self.default_app)
      register_page3_callbacks(self.default_app)