#!/usr/bin/python3.8
from flask import Flask, json, request, Response
import random
import datetime
import logging
from pymongo import MongoClient
import os
from dotenv import dotenv_values
from dotenv import load_dotenv
import dotenv
import requests


# some id global vars
name="Recipes"
app = Flask(name)

# logger configuraiton
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# common method to check env
def env_checker(list_vars):
    logger.info("Check environment definition:")
    all_ok=True
    for var in list_vars:
        if var in os.environ:
            logger.info("\t"+var+" :\tOK")
        else:
            logger.error("\t"+var+" :\tERROR - Not defined")
            all_ok=False
    return all_ok

# load configuraiton from mongodb
def load_configuration():
    if env_checker(["configuration"]):
        return json.loads(os.environ["configuration"])
    else:
        env_checker(["mongo_user","mongo_password","mongo_instance","environment","project"])
        mongo_user=os.environ["mongo_user"]
        mongo_password=os.environ["mongo_password"]
        mongo_instance=os.environ["mongo_instance"]
        mongo_database=os.environ["project"]+"-configurations"

        # Get :
        client = MongoClient("mongodb+srv://"+mongo_user+":"+mongo_password+"@"+mongo_instance+".bgg4gde.mongodb.net/?retryWrites=true&w=majority")
        # db = client.test
        id_ok={'identification': {'environment': 'local', 'project': 'codenito-use-case'} }
        id =  { 
            #    'identification': {'environment': 'local', 'project': 'codenito-use-case'} }
                'identification':{
                    'environment': os.environ["environment"]
                    # , 'project': os.environ["project"]
                    }
                }
        db = client.gettingStarted
        configurations = db.get_collection(mongo_database)
        logger.info ("Existing configurations")
        for configuration in configurations.find(id_ok):
        
            logger.info (configuration)
            return configuration
    return None


# mongo_user=os.environ["mongo_user"]
# mongo_password=os.environ["mongo_password"]
# mongo_instance=os.environ["mongo_instance"]

# read env from file
load_dotenv("environment.txt")

configuration=load_configuration()

def str_now():
    return str(datetime.datetime.now())

def get_sub_service(server, service):
    url=server+"/"+service
    print (str_now()+"\t"+"Guicher calls: "+url)
    # carrier = {}
    # TraceContextTextMapPropagator().inject(carrier)
    # header = {"traceparent": carrier["traceparent"]}
    header = {}
    x = requests.get(url,headers=header)  
    print (x.text)
    return x.text

@app.route('/hello', methods=['GET'])
def hello():
    logger.info (str_now()+"\t"+name+" says: Hello World")
    return str_now()+"\t"+name+" says: Hello World\n"

@app.route('/ask_for_pizza', methods=['GET'])
def get_ask_for_pizza():
    output=[]
    recipe = json.loads(get_sub_service( configuration['services']['recipes'], "get_random_recipe"))
    get_sub_service( configuration['services']['guichet'], "pizza"+"?name="+recipe['name'])

    return "OK"

# @app.route('/get_random_recipe', methods=['GET'])
# def get_random_recipe():
#     print (str_now()+"\t"+name+"\tchoose pizza")
#     index=random.randint(0, len(recipes)-1)
#     logger.info (str_now()+"\t"+name+"\tChoosen: "+str(index)+" > "+str(recipes[index]))
#     return recipes[index]

# @app.route('/get_recipe', methods=['GET'])
# def get_recipe():
#     # print(name)
#     # print(request.args)
#     for recipe in recipes:
#         print (" >"+recipe['name'])
#         if recipe['name'] == request.args['name']:
#             logger.info ("Return : "+recipe|'name')
#             return recipe
#     return "Nothing...."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
