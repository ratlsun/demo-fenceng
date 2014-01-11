# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
from demodao import Dao
import time
import atexit

def cleanup():
    db.removeOrder()

atexit.register(cleanup)

app = Flask(__name__)
db = Dao()

@app.before_request
def before_request():
    if request.path != '/':
        if not request.headers['content-type'].find('application/json'):
            return 'Unsupported Media Type', 415
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jquery/')
def jquery():
    return render_template('jquery.min.js')

@app.route('/payfor/')
def payfor():
    return render_template('payfor.html')

@app.route('/deliver/')
def deliver():
    return render_template('deliver.html')

@app.route('/iframe/')
def iframe():
    return render_template('iframe.html')

@app.route('/init/', methods=['GET'])
def init():
    ret_data = db.getItemsFromOrder()
    #print ret_data
    return jsonify(AllProducts=ret_data)

@app.route('/echo/', methods=['GET'])
def echo():
    pname = request.args.get('ProductName')
    pquan = request.args.get('Quantity')
    db.addItemToOrder(pname, pquan)
    time.sleep(3)
    ret_data = db.getItemsFromOrder()
    #print ret_data
    return jsonify(ProductName=pname, Quantity=pquan, AllProducts=ret_data)

@app.route('/remove/', methods=['GET'])
def remove():
    pid = request.args.get('Pid')
    db.delItemFromOrder(pid)
    ret_data = db.getItemsFromOrder()
    #print ret_data
    return jsonify(AllProducts=ret_data)

if __name__ == '__main__':
    app.run(port=8000, debug=True, threaded=True)
