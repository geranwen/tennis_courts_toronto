import dash
from dash import dcc
from dash import html
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Input, Output
from fuzzywuzzy import process

# Load your data
df = pd.read_csv('tennis_courts_toronto_full_cleaned_v2.csv')
# modify col `winter_play` in df so that empty cell are filled with `No`
df['winter_play'] = df['winter_play'].fillna('No')

# Create a Dash instance
app = dash.Dash(__name__)

# add this line to expose the flask server instance as the server. 
server = app.server

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Tennis Courts in Toronto - 20230916'),
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Enter a place name'
        ),
        html.Div(id='search-output')
    ]),
    html.Div([
        html.Label('Select Type:'),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': i, 'value': i} for i in df['type'].unique()],
            multi=True
        ),
    ]),
    html.Div([
        html.Label('Select Lights:'),
        dcc.Dropdown(
            id='lights-dropdown',
            options=[{'label': i, 'value': i} for i in df['lights'].unique()],
            multi=True
        ),
    ]),
    html.Div([
        html.Label('Select Courts:'),
        dcc.Dropdown(
            id='courts-dropdown',
            options=[{'label': i, 'value': i} for i in df['courts'].unique()],
            multi=True
        ),
    ]),
    html.Div([
        html.Label('Winter Play Available:'),
        dcc.Dropdown(
            id='winter-play-dropdown',
            options=[{'label': i, 'value': i} for i in df['winter_play'].dropna().unique()],
            multi=True
        ),
    ]),
    dl.Map(id='map', center=[df['latitude'].mean(), df['longitude'].mean()], zoom=11, children=[
        dl.TileLayer(),
    ], style={'width': '100%', 'height': '85vh', 'margin': "auto", "display": "block"}),
])

# Update the map based on the search input
@app.callback(
    Output('map', 'children'),
    [Input('search-input', 'value'),
     Input('type-dropdown', 'value'),
     Input('lights-dropdown', 'value'),
     Input('courts-dropdown', 'value'),
     Input('winter-play-dropdown', 'value')]
)
def update_output(value, selected_types, selected_lights, selected_courts, selected_winter_play):
    if not selected_types:
        selected_types = df['type'].unique().tolist()
    if not selected_lights:
        selected_lights = df['lights'].unique().tolist()
    if not selected_courts:
        selected_courts = df['courts'].unique().tolist()
    if not selected_winter_play:
        selected_winter_play = df['winter_play'].dropna().unique().tolist()

    filtered_df = df[df['type'].isin(selected_types) & df['lights'].isin(selected_lights) 
                     & df['courts'].isin(selected_courts) & df['winter_play'].isin(selected_winter_play)]

    if value is None or value == '':
        # If the search box is empty, display all markers
        markers = [
            dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(children=[
                    html.Div([
                        html.Div(f"Place: {place}"),
                        html.Div(f"Type: {typ}"),
                        html.Div(f"Lights: {lights}"),
                        html.Div(f"Courts: {courts}"),
                        html.Div(f"Winter Play: {winter_play if pd.notna(winter_play) else 'No'}")
                    ])
                ])
            ]) for lat, lon, place, typ, lights, courts, winter_play in zip(
                filtered_df['latitude'], filtered_df['longitude'], filtered_df['place'], filtered_df['type'], 
                filtered_df['lights'], filtered_df['courts'], filtered_df['winter_play']
            )
        ]
    else:
        # If there's a search term, find the best match and display only that marker
        best_match = process.extractOne(value, filtered_df['place'].tolist())
        if best_match:
            matched_row = filtered_df[filtered_df['place'] == best_match[0]]
            markers = [
                dl.Marker(position=[matched_row['latitude'].values[0], matched_row['longitude'].values[0]], children=[
                    dl.Tooltip(children=[
                        html.Div([
                            html.Div(f"Place: {matched_row['place'].values[0]}"),
                            html.Div(f"Type: {matched_row['type'].values[0]}"),
                            html.Div(f"Lights: {matched_row['lights'].values[0]}"),
                            html.Div(f"Courts: {matched_row['courts'].values[0]}"),
                            html.Div(f"Winter Play: {matched_row['winter_play'].values[0] if pd.notna(matched_row['winter_play'].values[0]) else 'No'}")
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
