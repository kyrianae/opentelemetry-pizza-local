#!/usr/bin/python3.8
from flask import Flask, json, request, Response
import random
import os
import requests
import datetime
import logging
from pymongo import MongoClient
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
from dotenv import dotenv_values
from dotenv import load_dotenv

from flask import Flask, request
  
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import metrics

from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# provider = TracerProvider()
# trace.set_tracer_provider(provider)
# tracer = trace.get_tracer(__name__)
# # Acquire a meter.
# meter = metrics.get_meter(__name__)

# some id global vars
name="Guichet"
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
    print (str_now()+"\t"+name+" calls: "+url)
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)
    header = {"traceparent": carrier["traceparent"]}
    # header = {}
    x = requests.get(url,headers=header)  
    print (x.text)
    return x.text

# FlaskInstrumentor().instrument_app(app)
# tracer = trace.get_tracer(__name__)
# # Acquire a meter.
# meter = metrics.get_meter(__name__)


    
@app.route('/hello', methods=['GET'])
def hello():
    return str_now()+"\t"+name+" says: Hello World\n"

@app.route('/pizza', methods=['GET'])
def pizza():
    pizza_name=request.args['name']
    # print (str_now()+"\t"+name+"\customer asked pizza")
    out=get_sub_service(configuration['services']['pizzaiolo'], "/make_pizza"+"?name="+pizza_name)
    print (str_now()+"\t"+pizza_name+"\t\tPizza delivered")
    return out+"\n"+str_now()+"\t"+pizza_name+"\t\tPizza delivered\n"
    
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
