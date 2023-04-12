#!/usr/bin/python3.8
from flask import Flask, json, request, Response
import random
import datetime

name="Hoover"
app = Flask(name)

def str_now():
    return str(datetime.datetime.now())

@app.route('/hello', methods=['GET'])
def hello():
    print (str_now()+"\t"+name+" says: Hello World")
    return str_now()+"\t"+name+" says: Hello World\n"

@app.route('/cook', methods=['GET'])
def cook():
    action="cooked"
    print (str_now()+"\t"+name+"\t"+action)
    return str_now()+"\t"+name+"\t"+action+"\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
