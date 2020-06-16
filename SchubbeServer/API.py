
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template, Response, request
import commander

global api
app = Flask(__name__)

class API:
    def __init__(self, addr, queues):
        self.addr = addr
        self.queues = queues



def start(addr, queues):
    global api
    api = API(addr, queues)
    app.run(host=addr, debug=True, threaded=True)


###################### API ######################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def getInput():
    if request.is_json:
        global api
        json = request.get_json()
        # user = json["user"]
        command = json["command"]

        commander.dispatchCommand(command, api.queues)
        print("TESST")

        # print("data = " + str(json))
    return "Posted"



