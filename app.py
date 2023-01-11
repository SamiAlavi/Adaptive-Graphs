from exporter import Exporter
from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
import json
import os
import sys
from NullIO import NullIO
from graph_networkx import NetworkX
from graph_graphviz import GraphViz
from graph_pyvis import Pyvis
from parser_standards import Parser

app = Flask(__name__, static_folder='build')
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.errorhandler(Exception)
# handle all other exception
def all_exception_handler(error):
    return error_response(500, str(error))

def error_401_handler(error):
    return error_response(401, "Unauthorized")

def error_response(status_code: int, error_message: str):
    res = {"error": error_message}
    return send_response(status_code, res)

def send_response(status_code: int, res: dict):
    return Response(status=status_code, mimetype="application/json", response=json.dumps(res))

@app.before_request 
def before_request_callback():
    method = request.method 
    path = request.path
         
    if (method=="POST" and (path.startswith("/graph") or path.startswith("/export"))):
        error_message = validate_graph()
        if (error_message):
            return error_response(400, error_message)

def validate_graph() -> str:
    graph_content_type = 'application/json'
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
        

@app.route("/graph/networkx", methods=['POST'])
def networkx() -> str:
    graph = NetworkX()
    graph.read_network_json(request.json)
    graph.create_graph()
    graph.draw_graph()
    image_base64 = graph.get_graph_data()
    return image_base64

@app.route("/graph/graphviz", methods=['POST'])
def graphviz() -> str:
    graph = GraphViz()
    graph.read_network_json(request.json)
    graph.create_graph()
    image_base64 = graph.get_graph_data()
    return image_base64

@app.route("/graph/pyvis", methods=['POST'])
def pyvis() -> str:
    options = {}
    try:
        options = request.json["options"]
    except:
        pass
    graph = Pyvis(options)
    graph.read_network_json(request.json)
    graph.create_graph()
    image_html = graph.get_graph_data()
    return image_html

@app.route("/parse", methods=['POST'])
def parse() -> str:
    key = "File"
    file = request.files.get(key)
    if (file):
        return Parser.parse(file)
    raise Exception(f"No file in form data with key '{key}' found")

@app.route("/export", methods=['POST'])
def parse_gml() -> str:
    exporter = Exporter()
    return exporter.export(request.json)    

app.register_error_handler(401, error_401_handler)

# @app.route("/", methods=['GET'])
# def home() -> str:
#     return "Hello, Flask!"

# Serve App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

debug = False
if __name__ == '__main__':
    if (not debug):
        sys.stdout = NullIO()
    app.run(debug=debug)