import json
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)


def solveproblem(req):

    return res


@app.route('/')
def hello_world():
    return 'Es funzt!'


@app.route('/packaging', methods=['POST'])
def packaging():
    answer = solveproblem(request.json)
    return answer


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        with open(sys.argv[1]) as json_file:
            data = json.load(json_file)
        answer = solveproblem(data)
        print(answer)
    else:
        app.run(host='0.0.0.0')