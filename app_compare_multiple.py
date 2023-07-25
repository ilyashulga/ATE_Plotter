import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os


# Function to load dataframes from Excel files in the exports_to_compare folder
def load_dataframes(folder_path):
    dataframes = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, engine='openpyxl', skiprows=4)
            dataframes[file_name] = df
    return dataframes

# Load dataframes from Excel files in the exports_to_compare folder
folder_path = 'exports_to_compare'
dataframes = load_dataframes(folder_path)

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Histogram Comparison"),
    
    # Dropdown to select column for histogram
    html.Label("Select column(s) for histogram:"),
    dcc.Dropdown(
        id='columns-for-histogram',
        options=[{'label': col, 'value': col} for col in dataframes[list(dataframes.keys())[0]].columns],
        value=[dataframes[list(dataframes.keys())[0]].columns[0]],  # Set the default value to the first column
        multi=True  # Allow multiple selections
    ),
    
    # Input for bin size
    html.Label("Select bin size:"),
    dcc.Input(
        id='bin-size',
        type='number',
        value=0.1  # Set the default bin size
    ),

    # Input for excluding values above
    html.Label("Exclude values above:"),
    dcc.Input(
        id='exclude-above',
        type='number',
        value=None
    ),

    # Input for excluding values below
    html.Label("Exclude values below:"),
    dcc.Input(
        id='exclude-below',
        type='number',
        value=None
    ),
    
    # Graph to display the histogram
    dcc.Graph(id='histogram-graph')
])

# Define the callback to update the graph based on user selections
@app.callback(
    Output('histogram-graph', 'figure'),
    [Input('columns-for-histogram', 'value'),
     Input('bin-size', 'value'),
     Input('exclude-above', 'value'),
     Input('exclude-below', 'value')]
)
def update_histogram(columns, bin_size, exclude_above, exclude_below):
    # Create traces for histograms
    traces = []
    for file_name, df in dataframes.items():
        for column in columns:
            # Apply exclusions if provided by the user
            if exclude_above is not None:
                df = df[df[column] <= exclude_above]
            if exclude_below is not None:
                df = df[df[column] >= exclude_below]

            trace = go.Histogram(
                x=df[column],
                xbins=dict(start=min(df[column]), end=max(df[column]), size=bin_size),  # Specify absolute bin size
                opacity=0.5,
                name=f'{file_name} - {column}'
            )
            traces.append(trace)

    # Define the layout for the graph
    layout = go.Layout(
        title="Histogram Comparison",
        xaxis=dict(title="Value"),
        yaxis=dict(title="Frequency"),
        barmode='overlay',  # Overlay histograms
        bargap=0.1,  # Gap between bars
        bargroupgap=0.2,  # Gap between histogram groups
        showlegend=True,  # Show legend
    )

    # Create the figure and return it
    fig = go.Figure(data=traces, layout=layout)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
