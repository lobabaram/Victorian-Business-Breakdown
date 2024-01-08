import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pandas
import dash_bootstrap_components as dbc
import statistics
import json


# Initial Values
BusSizeList = [
    'Non employing',
    '1-4 Employees',
    '5-19 Employees',
    '20-199 Employees',
    '200+ Employees'
]

# Read in VIC Data from csv
data = pandas.read_csv("vicdata.csv")

# Updated for filtered data
longs = data['Longitude'].tolist()
lats = data['Latitude'].tolist()
meanLong = statistics.mean(longs)
meanLat = statistics.mean(lats)


# Sample GeoJSON file (replace 'your_geojson_file.geojson' with your actual file)
# with open('index.json') as user_file:
#     geojson_file = user_file.read()
with open('index.json', 'r') as json_file:
    geojson_file = json.load(json_file)


# Initialize the Dash app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SUPERHERO],
                )
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Business Size and Industry Data Visualization"),
    html.Div([
        html.Label('Select Business Size:'),
        dcc.Dropdown(
            id='business-size-dropdown',
            style={'color': 'black'},
            options = [{"label": b ,"value": b} for b in BusSizeList],
            value='1-4 Employees',
            multi=False
        ),
    ]),
    html.Div([
        html.Label('Select Industry:'),
        dcc.Dropdown(
            id='industry-dropdown',
            style={'color': 'black'},
            options=[
                {'label': industry, 'value': industry}
                for industry in data['Industry Label'].unique()
            ],
            value='Manufacturing',
            multi=False
        ),
    ]),
    # App Container
        html.Div(
            id="app-container",
            children=[
                # Left Column ------------------------------------#
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="choropleth-container",
                            children=[
                                html.Div(
                                    [
                                        html.H5(id="map-title"),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "width": "100%"
                                    },
                                    className="eight columns",
                                ),
                                dcc.Graph(
                                    id="choropleth-map",
                                    style={
                                        # "display": "inline-block",
                                        # "padding": "20px 10px 10px 40px",
                                        "width": "100%",
                                        "height":"80vh",
                                    }                                          
                                        ),
                            ],
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "padding": "20px 10px 10px 40px",
                        "width": "45%",
                        "height":"60vh",
                    },
                    className="seven columns",
                ),
                # Right Column ------------------------------------#

                html.Div(
                    id="right-column",
                    children=[
                        html.Div(
                            id="bar-container",
                            children=[
                                html.Div(

                                            [
                                                html.H5(id="graph-title"),
                                            ],
                                            style={
                                                "display": "inline-block",
                                                # "width": "45%",
                                                "height":"85%",
                                            },
                                            className="eight columns",

                                ),
                                dcc.Graph(
                                    id="industry-breakdown-graph",
                                    style={
                                        # "display": "inline-block",
                                        # "padding": "20px 10px 10px 40px",
                                        "width": "100%",
                                        "height":"80vh",
                                    }                                     
                                          ),
                            ],
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "padding": "20px 10px 10px 40px",
                        "width": "52%",
                        "height":"100vh",
                    },
                    className="eight columns",
                ),
            ],
            className="row",
            style={"width": "100%", "height": "50vh", "margin": 0},
        )

])

# Define the callback to update the choropleth map and title
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('map-title', 'children')],
    [Input('business-size-dropdown', 'value'),
     Input('industry-dropdown', 'value')]
)
def update_choropleth_map(selected_business_size, selected_industry):
    # filtered_data = data[(data['Industry Label'] == selected_industry) & (data[selected_business_size] > 0)]
    filtered_data = data[(data['Industry Label'] == selected_industry)]


    fig = px.choropleth_mapbox(filtered_data,
                               geojson=geojson_file,
                               locations='LGA',
                               featureidkey="id",
                               color=selected_business_size,
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=7, center={"lat": meanLat, "lon": meanLong},
                               opacity=0.5,
                               custom_data=['LGA Label','POPULATION','METRO'],
                               labels={selected_business_size: f'{selected_business_size} Businesses'}
                               )
    # Update hover template to include custom data
    hover_template = ('<b>Region:</b> %{location}<br>'
                    #   f'<b>{selected_business_size}:</b> %{{color}}<br>'
                      '<b>LGA Name:</b> %{customdata[0]}<br>'
                      '<b>Population:</b> %{customdata[1]:,.0f}<br>'
                      '<b>Metro:</b> %{customdata[2]}'
                      )

    fig.update_traces(hovertemplate=hover_template)

    title = f"Choropleth Map: {selected_business_size} Businesses in {selected_industry}"
    return fig, title

# Update Industry Breakdown Graph with postcode updates and graph-type
@app.callback(
    [Output('industry-breakdown-graph', 'figure'),
    Output('graph-title','children')],
    [Input('choropleth-map', 'clickData'),
     Input('business-size-dropdown', 'value')],
)
# @cache.memoize(timeout=cfg["timeout"])
def update_industry_breakdown(click_data,business_size):
    if click_data is None or business_size is None:
        # if no region is clciked, return an empty bar graph
        default_fig = px.bar()  # You may want to customize this for a default view
        default_title = "Select a region and business size to see the breakdown"
        return default_fig,default_title

    clicked_region = click_data['points'][0]['customdata'][0]
    filtered_data = data[data['LGA Label'] == clicked_region]

    fig= px.bar(
        filtered_data,
        x = 'Industry Label',
        y= [business_size],
        # title=f'Industry Breakdown in {clicked_region}',
        labels={
            'value': 'Number of Businesses',
            'variable': 'Business Size',
        })
    title = f'Industry Breakdown in {clicked_region}'
    return fig,title


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
