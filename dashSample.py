import dash
import dash_table
from dash.dependencies import Input as ddInput
from dash.dependencies import Output as ddOutput
from dash.dependencies import State as ddState
import dash_core_components as dcc
import dash_html_components as html
import datetime
import os
import pandas as pd
from lib_TableReader import TableReader
from lib_DashUtilities import DashUtilities as du

def whereAmI():
    return os.path.dirname(os.path.abspath(__file__))
defaultDirectory = os.path.join(whereAmI(),'files')
fileDirectory = defaultDirectory
tableReader = None
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'
]
assetsFolder = os.path.join(whereAmI(), 'assets')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder=assetsFolder)

app.title = 'SAMPLE TITLE (PLEASE REPLACE)'
app.layout = html.Div(
    children=[
        html.Div(
            id='top',
            className = 'selectorDiv',
            children = [
                dcc.Input(id="ddInputFileDirectory", type="text", placeholder=defaultDirectory,style={'width':'400px'}, debounce=True),
				html.Button("Refresh", id='refreshButton',style = {'float':'left'}, n_clicks=0),
                dcc.Dropdown(id='ddInputFilesDirectoryDropdown',style = {'float':'left','width':'200px'}),
                html.Button("Update", id='updateButton',style = {'float':'left'}, n_clicks=0),
            ]
        ),
        html.Div(
            id='outputHolderDiv',
            className = 'selectorDiv',
            children = [
                html.Div(
                    id='outputDiv',
                    className = 'textDiv',
                    children = []
                )
            ]
        ),
        dcc.Graph(id='ddOutputMainGraph',style={'height':'80vh'},),
        dcc.Graph(id='ddOutputMainGraph2',style={'height':'80vh'},),
    ]
)

@app.callback(
    [
		ddOutput('ddInputFilesDirectoryDropdown', 'options'),
    ],
    [
		ddInput('ddInputFileDirectory', 'value'),
		ddInput('refreshButton', 'n_clicks'),
    ]
)
def loadFileList(dir, btn):
    global defaultDirectory
    global fileDirectory
    if(dir is None or dir==''):
        dir = defaultDirectory
    
    fileDirectory = dir
    try:
        fileList = [ os.path.basename(os.path.normpath(f.path)) for f in os.scandir(fileDirectory) ]
    except FileNotFoundError:
        fileDirectory = defaultDirectory
        fileList = [ os.path.basename(os.path.normpath(f.path)) for f in os.scandir(fileDirectory) ]
    dashFileList = du.generateDropdownList(fileList)
    return [dashFileList]

	
@app.callback(
    [
		ddOutput('outputDiv', 'children'),
    ],
    [
		ddInput('ddInputFilesDirectoryDropdown','value'),
		ddInput('updateButton', 'n_clicks'),
    ]
)
def loadFile(folder, btn):
    global tableReader
    if(tableReader == '' or folder == '' or folder is None):
        tableReader = None
        return ['No file sepected']
    tableReader = TableReader(os.path.join(fileDirectory,folder), autoDate = True)
    return ['Loaded: '+folder]

@app.callback(
    [
		ddOutput('ddOutputMainGraph', 'figure'),
		ddOutput('ddOutputMainGraph2', 'figure'),
    ],
    [
		ddInput('outputDiv','children'),
    ]
)
def generator(folder):
    firstColumnIndex = True
    global tableReader
    if(tableReader == None or tableReader == '' or folder == '' or folder is None):
        tableReader = None
        return [du.placeholderFigure(), du.placeholderFigure()]
    df = tableReader.getDf()
    columns = list(df.columns)
    if(firstColumnIndex):
        x = df[columns[0]]
        y = df[columns[1:]]
    else:
        x = df.index.values.tolist()
        y = df[columns]
    figure = du.generateFigure(data = du.generateData(x,y))
    return [figure,figure]


if __name__ == '__main__':
    app.run_server(debug=True)
    