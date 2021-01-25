from flask import Flask
from flask import jsonify
from flask import request
import json
import datetime
from flask import render_template
import socket
from flask_cors import CORS
import sys, getopt
import time

import Controller as cc

control = cc.Controller()

app = Flask(__name__)
CORS(app)

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

@app.route('/api/testAPI')
def testAPI():
    return jsonify({
        "return_status":"success",
        "return_message":"failed"
    })

@app.route('/api/ImageProcess',methods=['POST'])
def ImageProcess():
    req_data = request.get_json()
    proc = control.predicImage(req_data)
    print(proc)
    return jsonify(proc)

def main(argv):
    ipaddr = IPAddr
    portnum = 20031
    try:
        opts, args = getopt.getopt(argv,"l:p:",["ipchange=","portchange="])
        for opt, arg in opts:
            if opt in ("-l", "--ipchange"):
                ipaddr = arg
            elif opt in ("-p", "--portchange"):
                portnum = arg

        app.run(debug=True, host=ipaddr, port=portnum)
    except Exception as e:
        print(e)
        app.run(debug=True, host="0.0.0.0", port=20031)

if __name__ == "__main__":
    main(sys.argv[1:])


        
