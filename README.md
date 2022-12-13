# Adaptable Directed Graphs in the Web Browser

Web Engineering Seminar
 
# Installation

**Note: This project is using:**
- [Python 3.10](https://www.python.org/downloads/release/python-3100/)
- [pip](https://pypi.org/project/pip/)

Installing the dependencies of the main project, run following command:

``` pip install -r requirements.txt ```

Installing the dependencies for graph dummy data, run following command:

``` pip install -r "network generation/requirements.txt" ```

# Run Backend Server

After installing all the dependencies of project, run following command:

``` flask run ```

## Routes

Sample Request Body

<pre>
{
    "nodes": ["A", "B", "C"],
    "matrix": [
        [[0], [1], [2]],
        [[3], [4], [5]],
        [[6], [7], [8]]
    ]
}
</pre>

<table border="1">
    <tr>
        <td>Library</td>
        <td>Method</td>
        <td>Route</td>
        <td>Request</td>
        <td>Response</td>
    </tr>
    <tr>
        <td>NetworkX</td>
        <td>POST</td>
        <td>/graph/networkx</td>
        <td>JSON</td>
        <td>Image base64</td>
    </tr>
    <tr>
        <td>Graphviz</td>
        <td>POST</td>
        <td>/graph/graphviz</td>
        <td>JSON</td>
        <td>Image base64</td>
    </tr>
    <tr>
        <td>Pyvis</td>
        <td>POST</td>
        <td>/graph/pyvis</td>
        <td>JSON</td>
        <td>HTML page</td>
    </tr>
</table>

# Run Individual Files

After installing all the dependencies of project, run following command:

``` python {file_name}.py ```

where file_name is:
- graph_networkx
- graph_graphviz
- graph_pyvis