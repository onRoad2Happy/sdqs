import sys
import json
import feature_utils as fu
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'


@app.route('/profiling', methods=['POST'])
def profiling():
    data = json.loads(request.data)
    if 'id' not in data or 'platform' not in data:
        return 'you should provide both code and lang'

    table_name = data['table_name']
    data_type = data['type'] 
    result = fu.profiling(table_name, data_type)

    return jsonify(result)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port)

