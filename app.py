import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os
import base64

global dataframes

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
folder_path = 'exports'
dataframes = load_dataframes(folder_path)

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("Histogram Comparison"),
    dcc.Upload(
        id='upload-files',
        children=html.Button('Add Files'),
        multiple=True
        ),
    html.Div(id='output-upload'),
    html.Button('Delete All Files', id='delete-button'),
    html.Div(id='delete-output'),
    html.Div(id='folder-contents-output'),
    # Dropdown to select column for histogram
    html.Label("Select column(s) for histogram:"),
    dcc.Dropdown(
        id='columns-for-histogram',
        options=[{'label': col, 'value': col} for col in dataframes[list(dataframes.keys())[0]].columns],
        value=[dataframes[list(dataframes.keys())[0]].columns[2]],  # Set the default value to the first column
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
    dcc.Graph(id='histogram-graph'),
    # Standard deviation display
    html.Div(id='std-dev-output'),
    html.H2("Filter by Column and Value"),
    html.H3("Select Column"),
    # Dropdown for column selection
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in dataframes[list(dataframes.keys())[0]].columns],
        value=dataframes[list(dataframes.keys())[0]].columns[0]
    ),
    html.H3("Select Value"),
    # Input for filtering
    dcc.Input(
        id='filter-input',
        type='text',
        placeholder='Enter filter value...',
    ),
])


# Callback for file deletion
@app.callback(
    Output('delete-output', 'children'),
    [Input('delete-button', 'n_clicks')]
)
def delete_files(n_clicks):
    global dataframes
    if n_clicks:
        folder = 'exports'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                return f'Failed to delete {filename}. Reason: {e}'
        dataframes = load_dataframes(folder_path)
        return 'All files have been deleted!'
    return None

# Callback for files upload
@app.callback(
    Output('output-upload', 'children'),
    [Input('upload-files', 'contents'),
     Input('upload-files', 'filename')]
)
def save_uploaded_files(contents, filenames):
    global dataframes
    if contents is None:
        return []

    # Make sure 'exports' directory exists
    if not os.path.exists('exports'):
        os.makedirs('exports')

    # Iterate over each file and save
    messages = []
    for content, filename in zip(contents, filenames):
        # Check file format
        if not filename.endswith('.xlsx'):
            messages.append(html.Div(f"Skipped {filename}. Only .xlsx format is accepted."))
            continue

        data = content.encode("utf8").split(b";base64,")[1]
        filepath = os.path.join('exports', filename)

        # Save to 'exports' directory
        with open(filepath, "wb") as fp:
            fp.write(base64.b64decode(data))

        messages.append(html.Div(f"File {filename} saved successfully."))
    dataframes = load_dataframes(folder_path)
    return messages

# Define the callback to update the graph based on user selections
@app.callback(
    [Output('histogram-graph', 'figure'),
     Output('std-dev-output', 'children'),
     Output('folder-contents-output', 'children'),
     Output('columns-for-histogram', 'options'),
     Output('column-dropdown', 'options')
     ],
    [Input('columns-for-histogram', 'value'),
     Input('bin-size', 'value'),
     Input('exclude-above', 'value'),
     Input('exclude-below', 'value'),
     Input('column-dropdown', 'value'),
     Input('filter-input', 'value')]
)
def update_histogram(columns, bin_size, exclude_above, exclude_below, selected_column, filter_value):
    

    
    # Create traces for histograms
    traces = []

    std_dev_info = []

    for file_name, df in dataframes.items():
        if filter_value is not None:
            # Filtering the dataframe based on user input
            dff = df[df[selected_column].astype(str).str.contains(filter_value, case=False)]
        else:
            dff = df
        for column in columns:
            # Apply exclusions if provided by the user
            dff = dff[pd.to_numeric(dff[column], errors='coerce').notna()]
            if exclude_above is not None:
                dff = dff[dff[column] <= exclude_above]
            if exclude_below is not None:
                dff = dff[dff[column] >= exclude_below]
            #print(dff.shape[0])
            if not dff.empty:
                trace = go.Histogram(
                    x=dff[column],
                    xbins=dict(start=min(dff[column]), end=max(dff[column]), size=bin_size),  # Specify absolute bin size
                    #xbins=dict(start=df[pd.to_numeric(dff[column], errors='coerce').notna()], end=max(df[pd.to_numeric(dff[column], errors='coerce').notna()]), size=bin_size),  # Specify absolute bin size
                    opacity=0.5,
                    name=f'{file_name} - {column}'
                )
                traces.append(trace)
        
                # Calculate standard deviation for each column in each dataframe
            std_dev = dff[column].std()
            std_dev_info.append(f"{file_name} - {column} Std. Dev.: {std_dev:.2f}")

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

    files = os.listdir(folder_path)
    
    if not files:
        return 'The exports folder is empty.'
    return fig, html.Ul([html.Li(std) for std in std_dev_info]), html.Ul([html.Li(file) for file in files]), [{'label': col, 'value': col} for col in dataframes[list(dataframes.keys())[0]].columns], [{'label': col, 'value': col} for col in dataframes[list(dataframes.keys())[0]].columns]

# Run the app
if __name__ == '__main__':
    #app.run_server(port=8055)
    app.run(host="0.0.0.0", port=8055)
