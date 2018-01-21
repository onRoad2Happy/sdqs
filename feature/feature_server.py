import sys
import json
from flask import Flask
from flask import jsonify
from flask import request
import feature_utils as fu

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = json.loads(request.data)
    if 'id' not in data or 'platform' not in data:
        return 'you should provide both code and lang'

    id = data['id']
    cpu = data['cpu'] 
    memory = data['memory']
    platform = data['platform']
    instance = data['instance']
    region = data['region']
    zone = data['zone']
    amount = data['amount']
    duration = data['duration']


    print 'API got called with cpu %d, memory %d(GB), in %s platform with region %s and zone %s amount is %d duration is %d' % (cpu, memory, platform, region, zone, amount, duration)
    # return jsonify({'build': 'build from flask', 'run': 'hello from flask'})
    result = fu.evaluate(id, cpu, memory, platform, instance, region, zone, amount, duration)
    return jsonify(result)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port)


