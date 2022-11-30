from flask import Flask, request

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