#!/usr/bin/python3.8
from flask import Flask, json, request, Response
import random
import datetime
import logging

name="Recipes"
app = Flask(name)
print (__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def str_now():
    return str(datetime.datetime.now())

@app.route('/hello', methods=['GET'])
def hello():
    logger.info (str_now()+"\t"+name+" says: Hello World")
    return str_now()+"\t"+name+" says: Hello World\n"

recipes=[
    {"name":"margarita", "ingredients":["pie","tomato","cheese","mushroom","ham"]},
    {"name":"vegan", "ingredients":["pie","tomato","mushroom"]},
    {"name":"cheese","ingredients":["pie","cheese"]},
    {"name":"napolitana","ingredients":["pie","tomato"]}
]

@app.route('/list', methods=['GET'])
def get_list():
    output=[]
    for recipe in recipes:
        output.append(recipe['name'])
    return output

@app.route('/get_random_recipe', methods=['GET'])
def get_random_recipe():
    print (str_now()+"\t"+name+"\tchoose pizza")
    index=random.randint(0, len(recipes)-1)
    logger.info (str_now()+"\t"+name+"\tChoosen: "+str(index)+" > "+str(recipes[index]))
    return recipes[index]

@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    # print(name)
    # print(request.args)
    for recipe in recipes:
        print (" >"+recipe['name'])
        if recipe['name'] == request.args['name']:
            logger.info ("Return : "+recipe['name'])
            return recipe
    return "Nothing...."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
