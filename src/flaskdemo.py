# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
import time
app = Flask(__name__)
 
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
 
@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"ProductName": request.args.get('ProductName'),
                "Quantity": request.args.get('Quantity')

                }
    time.sleep(3)
    return jsonify(ret_data)
 
if __name__ == '__main__':
    app.run(port=8000, debug=True)
