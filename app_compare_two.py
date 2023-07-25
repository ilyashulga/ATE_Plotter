import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


# Load the Excel data using Pandas
df1 = pd.read_excel('1.xlsx', engine='openpyxl', skiprows=4)
df2 = pd.read_excel('2.xlsx', engine='openpyxl', skiprows=4)

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Histogram Comparison"),
    
    # Dropdown to select column for histogram
    html.Label("Select column(s) for histogram:"),
    dcc.Dropdown(
        id='columns-for-histogram',
        options=[{'label': col, 'value': col} for col in df1.columns],
        value=[df1.columns[0]],  # Set the default value to the first column
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
    # Create traces for file1 histograms
    traces_file1 = []
    for column in columns:
        trace_file1 = go.Histogram(
            x=df1[column],
            nbinsx=bin_size,
            opacity=0.5,
            name=f'File 1 - {column}'
        )
        traces_file1.append(trace_file1)

    # Create traces for file2 histograms
    traces_file2 = []
    for column in columns:
        trace_file2 = go.Histogram(
            x=df2[column],
            nbinsx=bin_size,
            opacity=0.5,
            name=f'File 2 - {column}'
        )
        traces_file2.append(trace_file2)

    # Define the layout for the graph
    layout = go.Layout(
        title="Histogram Comparison",
        xaxis=dict(title="Value"),
        yaxis=dict(title="Frequency"),
        barmode='overlay',  # Overlay histograms
        bargap=0.1,  # Gap between bars
        bargroupgap=0.2,  # Gap between histogram groups
        showlegend=True,  # Show legend
        grid=go.layout.Grid(rows=1, columns=2, pattern='independent'),  # Create subplots with shared x-axis
        margin=go.layout.Margin(l=50, r=50, b=50, t=80),  # Adjust margins
    )

    # Create the figure and return it with two subplots
    fig = go.Figure(data=traces_file1 + traces_file2, layout=layout)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8055, debug=True)
