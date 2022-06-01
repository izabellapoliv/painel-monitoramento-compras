#coding: utf-8

import os
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/compras", methods=["POST"])
def compras():
    input_json = request.get_json(force = True)
    dictToReturn = {'text': input_json['text'], 'mais': 'anem'}
    return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(debug = os.environ.get("DEBUG"), host = '0.0.0.0')
