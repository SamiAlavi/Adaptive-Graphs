from flask import Flask, request
from typing import Any
from graph_networkx import NetworkX

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)

@app.before_request 
def before_request_callback():
    method = request.method 
    path = request.path
         
    if (path.startswith("/api") and method == "POST"): 
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return 'Content-Type not supported!'

@app.route("/", methods = ['GET'])
def home() -> str:
    return "Hello, Flask!"

@app.route("/api/networkx", methods = ['POST'])
def networkx() -> Any:
    json = request.json
    graph = NetworkX()
    graph.read_network_json(json)
    graph.create_graph()
    fig = graph.draw_graph()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    response = output.getvalue()
    return Response(response, mimetype='image/png')