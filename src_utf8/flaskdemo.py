# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, Response, make_response
from demodao import Dao
import time
import atexit
import json

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

@app.route('/login')
def login():
    response = make_response(render_template('index.html'))
    response.set_cookie('username', 'Hale')
    return response

@app.route('/admin')
def admin():
    username = request.cookies.get('username')  
    if username == 'Hale':
        return Response(json.dumps({ 'result': 'SUCCESS'}), mimetype='text/html')
    else:
        return Response(json.dumps({ 'result': 'FOBIDDEN', 'reason': 'Only Hale can access. Please visit login first.'}), 
            403, mimetype='text/html')

@app.route('/api/products', methods=['GET'])
def listProducts():
    ret_data = db.getItemsFromOrder()
    #return jsonify(AllProducts=ret_data)
    return Response(json.dumps({'AllProducts':ret_data}),  mimetype='text/html')

@app.route('/api/products/<int:pid>', methods=['GET'])
def getProduct(pid):
    ret_data = db.getItemByIdFromOrder(pid)
    if ret_data == None:
        #return jsonify({ 'result': 'NOT FOUND'}), 404
        return Response(json.dumps({ 'result': 'NOT FOUND'}), 404, mimetype='text/html')
    #return jsonify(Product=ret_data)
    return Response(json.dumps({'Product':ret_data}),  mimetype='text/html')

@app.route('/api/products', methods=['POST'])
def createProduct():
    if not request.data:
        #return jsonify({ 'result': 'FAIL', 'reason': 'Empty post data.' }), 400
        return Response(json.dumps({ 'result': 'FAIL', 'reason': 'Empty post data.' }), 400, mimetype='text/html')
    print request.data
    pdata = json.loads(request.data)
    pname = pdata.get('ProductName', '')
    pquan = pdata.get('Quantity', 0)
    ret_data = db.addItemToOrder(pname, pquan)

    #for rf demo
    time.sleep(3) 

    #return jsonify(Product=ret_data), 201
    return Response(json.dumps({'Product':ret_data}), 201,  mimetype='text/html')

@app.route('/api/products/<int:pid>', methods=['PUT'])
def updateProduct(pid):
    if not request.data:
        #return jsonify({ 'result': 'FAIL', 'reason': 'Empty post data.' }), 400
        return Response(json.dumps({ 'result': 'FAIL', 'reason': 'Empty post data.' }), 400, mimetype='text/html')
    print request.data
    pdata = json.loads(request.data)
    pname = pdata.get('ProductName', '')
    pquan = pdata.get('Quantity', 0)
    ret_data = db.updateItemToOrder(pid, pname, pquan)
    #return jsonify(Product=ret_data)
    return Response(json.dumps({'Product':ret_data}),  mimetype='text/html')

@app.route('/api/products/<int:pid>', methods=['DELETE'])
def deleteProduct(pid):
    db.delItemFromOrder(pid)
    #return jsonify({ 'result': 'SUCCESS' })
    return Response(json.dumps({ 'result': 'SUCCESS' }),  mimetype='text/html')

if __name__ == '__main__':
    app.run(port=8000, debug=True, threaded=True)
