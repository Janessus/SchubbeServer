
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template, Response, request

global api

app = Flask(__name__)
api = None

class API:
    def __init__(self, addr, queues):
        self.addr = addr
        self.queues = queues
        self.start()
        api = self

    def start(self):
        app.run(host=self.addr, debug=True, threaded=True)


###################### API ######################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/command', methods=['POST'])
def getInput():
    if request.is_json:
        json = request.get_json()
        inputType = json["inputType"]

        # print("data = " + str(json))
    return "Posted"



