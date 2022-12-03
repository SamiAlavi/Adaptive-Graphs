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

### NetworkX

- POST Method
- /graph/networkx

### Graphviz

- POST Method
- /graph/graphviz

# Run Individual Files

After installing all the dependencies of project, run following command:

``` python {file_name}.py ```

where file_name is:
- graph_networkx
- graph_graphviz
- graph_pyvis