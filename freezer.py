#!/usr/bin/python3.8
from flask import Flask, json, request, Response
import random
import datetime

app = Flask("pizzaiolo")
name="Freeze"
def str_now():
    return str(datetime.datetime.now())

@app.route('/hello', methods=['GET'])
def hello():
    print (str_now()+"\t"+name+"says: Hello World")
    return str_now()+"\t"+name+"says: Hello World\n"

@app.route('/pie', methods=['GET'])
def pie():
    print (str_now()+"\t"+name+"\tpie")
    return str_now()+"\t"+name+"\tpie\n"

@app.route('/cheese', methods=['GET'])
def cheese():
    print (str_now()+"\t"+name+"\tcheese")
    return str_now()+"\t"+name+"\tcheese\n"

@app.route('/tomato', methods=['GET'])
def tomato():
    print (str_now()+"\t"+name+"\ttomato")
    return str_now()+"\t"+name+"\ttomato\n"

@app.route('/ham', methods=['GET'])
def ham():
    print (str_now()+"\t"+name+"\tham")
    return str_now()+"\t"+name+"\tham\n"

@app.route('/mushroom', methods=['GET'])
def mushroom():
    print (str_now()+"\t"+name+"\tmuhsroom")
    return str_now()+"\t"+name+"\tmushroom\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)
