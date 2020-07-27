import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go
from collections import deque
import math
import serial
import re


def sensor():
    ser = serial.Serial('COM4', baudrate=115200, timeout=1)
    return ser


def dataCollector():
    ser =sensor()
    sensorData = ser.readline().decode('ascii')
    y,z=0.0,0.0
    try:
        y,z=re.findall('\d+\.\d+|\d+', sensorData)
        print(y,z)
    except:
        print('Couldn\'t find numerical values using regex')
    return [y,z]


X = deque(maxlen=10)
X.append(1)
Y = deque(maxlen=10)
Y.append(1)

app = dash.Dash(__name__)

colors = {
    'background': 'white',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Esp32: Hall Sensor Realtime Chart',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='The integrated Hall Sensor on the esp32 is\
             used to detect the presence of magnetism \n then via the \
             serial port it transfers its data readings in realtime,\
             finally all data is presented in a live chart using dash (python).', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(
        [
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=1000,
                n_intervals=0
            ),
        ]
    )


])


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])


def update_graph_scatter(n):
    global X
    global Y
    global Z
    
    X.append(X[-1]+1)
    #local_magnetism,internal_temperature = dataCollector()
    #Y.append(float(internal_temperature))
    #Z.append(float(local_magnetism))
    Y.append(Y[-1]+1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(X), y=list(Y),
                    mode='lines+markers',
                    name='lines',
                    line=dict(color='blue', width=4)))
                  
    fig.add_trace(go.Scatter(x=list(X), y=list(Y),
                    mode='lines',
                    name='lines',
                    line=dict(color='firebrick', width=4)))

       
    return {'data': [fig], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y), max(Y)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)
    

    
