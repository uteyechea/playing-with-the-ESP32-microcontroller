import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque

import serial
import re


def sensor():
    ser = serial.Serial('COM4', baudrate=115200, timeout=1)
    return ser


def dataCollector():
    ser = sensor()
    data = ser.readline().decode('ascii')
    findObj = re.search(r'(\d+)', data)
    if findObj:
        y = float(findObj.group())
        return y


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
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
    X.append(X[-1]+1)
    data = float(dataCollector())
    Y.append(data)
    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                yaxis=dict(range=[min(Y), max(Y)]),)}


if __name__ == '__main__':
    sensor()
    app.run_server(debug=True)
    

    
