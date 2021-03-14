import json
import sys
from flask import Flask, request, jsonify

from pathfinding import Network

app = Flask(__name__)


def pathfinding(req):

    cap = req['cap']
    pickpool = req['pickpool']

    graph = req['graph']
    nodes = graph['nodes']
    edges = graph['edges']

    network = Network(nodes, edges, pickpool, cap)
    return json.dumps(network.solve())


@app.route('/')
def hello_world():
    return 'Es funzt!'


@app.route('/pathfinding', methods=['POST'])
def packaging():
    answer = pathfinding(request.json)
    return answer


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        with open(sys.argv[1]) as json_file:
            data = json.load(json_file)
        answer = pathfinding(data)
        print(answer)
    else:
        app.run(host='0.0.0.0')