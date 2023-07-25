import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Load the Excel data using Pandas
df = pd.read_excel('1.xlsx', engine='openpyxl', skiprows=4)

print(df.head())

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Histogram Plot"),
    
    # Dropdown to select column for histogram
    html.Label("Select column(s) for histogram:"),
    dcc.Dropdown(
        id='columns-for-histogram',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=[df.columns[0]],  # Set the default value to the first column
        multi=True  # Allow multiple selections
    ),
    
    # Input for bin size
    html.Label("Select bin size:"),
    dcc.Input(
        id='bin-size',
        type='number',
        value=10  # Set the default bin size
    ),
    
    # Graph to display the histogram
    dcc.Graph(id='histogram-graph')
])

# Define the callback to update the graph based on user selections
@app.callback(
    Output('histogram-graph', 'figure'),
    [Input('columns-for-histogram', 'value'),
     Input('bin-size', 'value')]
)
def update_histogram(columns, bin_size):
    # Create a list of histogram traces for each selected column
    traces = []
    for column in columns:
        trace = go.Histogram(
            x=df[column],
            nbinsx=bin_size,
            opacity=0.5,
            name=column
        )
        traces.append(trace)

    # Define the layout for the graph
    layout = go.Layout(
        title="Histogram Plot",
        xaxis=dict(title="Value"),
        yaxis=dict(title="Frequency"),
        barmode='overlay',  # Overlay multiple histograms on the same graph
    )

    # Create the figure and return it
    return {'data': traces, 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
