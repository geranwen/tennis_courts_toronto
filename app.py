### RUN THIS UNDER 'trt_tennis' ENVIRONMENT
###

import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html

import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Input, Output
from fuzzywuzzy import process

# Load your data
df = pd.read_csv('tennis_courts_toronto_full_cleaned_v2.csv')

# Create a Dash instance
app = dash.Dash(__name__)

# add this line to exposre the flask server instance as the server. 
server = app.server

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Tennis Courts in Toronto'),
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Enter a place name'
        ),
        html.Div(id='search-output')
    ]),
    dl.Map(id='map', center=[df['latitude'].mean(), df['longitude'].mean()], zoom=10, children=[
        dl.TileLayer(),
    ], style={'width': '100%', 'height': '85vh', 'margin': "auto", "display": "block"}),
])

# Update the map based on the search input
@app.callback(
    Output('map', 'children'),
    [Input('search-input', 'value')]
)
def update_output(value):
    if value is None or value == '':
        # If the search box is empty, display all markers
        markers = [
            dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(children=[
                    html.Div([
                        html.Div(f"Place: {place}"),
                        html.Div(f"Type: {typ}"),
                        html.Div(f"Lights: {lights}"),
                        html.Div(f"Courts: {courts}")
                    ])
                ])
            ]) for lat, lon, place, typ, lights, courts in zip(
                df['latitude'], df['longitude'], df['place'], df['type'], df['lights'], df['courts']
            )
        ]
    else:
        # If there's a search term, find the best match and display only that marker
        best_match = process.extractOne(value, df['place'].tolist())
        if best_match:
            matched_row = df[df['place'] == best_match[0]]
            markers = [
                dl.Marker(position=[matched_row['latitude'].values[0], matched_row['longitude'].values[0]], children=[
                    dl.Tooltip(children=[
                        html.Div([
                            html.Div(f"Place: {matched_row['place'].values[0]}"),
                            html.Div(f"Type: {matched_row['type'].values[0]}"),
                            html.Div(f"Lights: {matched_row['lights'].values[0]}"),
                            html.Div(f"Courts: {matched_row['courts'].values[0]}")
                        ])
                    ])
                ])
            ]
        else:
            markers = []
    return [dl.TileLayer()] + markers

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)