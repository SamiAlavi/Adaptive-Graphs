from flask import Flask, request
from typing import Any
from graph_networkx import NetworkX

app = Flask(__name__)

graph_content_type = 'application/json'

@app.before_request 
def before_request_callback():
    method = request.method 
    path = request.path
         
    if (path.startswith("/graph") and method == "POST"): 
        content_type = request.headers.get('Content-Type')
        if (content_type != graph_content_type):
            return f'Content-Type should be "{graph_content_type}"!'
        if (not ("nodes" in request.json and "matrix" in request.json)):
            return f'Request body JSON should have "nodes" and "matrix"'
        nodes = request.json["nodes"]
        matrix = request.json["matrix"]
        num_nodes = len(nodes)
        rows_matrix = len(matrix)
        if (rows_matrix < num_nodes):            
            return f"Matrix shape is not correct. Minimum required: ({num_nodes}, {num_nodes})"
        for row in matrix:
            if (len(row) < num_nodes):
                return f"Matrix shape is not correct. Minimum required: ({num_nodes}, {num_nodes})"
        

@app.route("/", methods=['GET'])
def home() -> str:
    return "Hello, Flask!"

@app.route("/graph/networkx", methods=['POST'])
def networkx() -> str:
    graph = NetworkX()
    graph.read_network_json(request.json)
    graph.create_graph()
    fig = graph.draw_graph()
    image_html = graph.get_graph_image(fig)
    return image_html

if __name__ == '__main__':
    app.run(debug=False)