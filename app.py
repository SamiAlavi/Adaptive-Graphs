from flask import Flask, request
from typing import Any
from graph_networkx import NetworkX

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
def networkx() -> str:
    graph = NetworkX()
    graph.read_network_json(request.json)
    graph.create_graph()
    fig = graph.draw_graph()
    image_html = graph.get_graph_image(fig)
    return image_html

if __name__ == '__main__':
    app.run(debug=False)