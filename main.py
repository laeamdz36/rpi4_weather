"""Module for build dash app for reaspberry PI"""
import asyncio
import datetime as dt
from flask import Flask
import dash
from dash import dcc, html
import plotly.graph_objs as go
import uvicorn
from dash import Input, Output
from dash.dash import Dash

# Crear la aplicación Flask
app = Flask(__name__)

# Crear la aplicación Dash compatible con Flask
dash_app = Dash(__name__, server=app, routes_pathname_prefix="/dashboard/")

# Configurar Dash con un gráfico en vivo
dash_app.layout = html.Div([
    html.H1("Monitor de Datos en Tiempo Real"),
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="interval-update", interval=1000, n_intervals=0)
])

# Almacenamos los datos recibidos por WebSocket
data_store = {"x": [], "y": []}

# WebSocket para enviar datos


@app.route('/ws')
def websocket_endpoint():
    # WebSocket no es compatible nativamente con Flask, por lo que usaríamos una librería adicional
    # Para simplificar este ejemplo, este endpoint no es funcional sin una librería que soporte WebSockets en Flask.
    pass

# Callback para actualizar el gráfico en Dash


@dash_app.callback(
    Output("live-graph", "figure"),
    [Input("interval-update", "n_intervals")]
)
def update_graph(_):
    return {
        "data": [go.Scatter(x=data_store["x"], y=data_store["y"], mode="lines", name="Valor")],
        "layout": go.Layout(title="Datos en Tiempo Real", xaxis=dict(title="Tiempo"), yaxis=dict(title="Valor"))
    }


# Ejecutar la aplicación Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
