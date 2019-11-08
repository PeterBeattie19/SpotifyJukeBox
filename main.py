import time
from pprint import pprint
from json_database import JsonDatabase

db = JsonDatabase("database.json")


''' 
from flask import Flask, escape, request 


app = Flask(__name__) 


@app.route('/')
def hello():
    name = request.args.get("name", "World") 
    return f'hello {escape(name)}!' 
'''
