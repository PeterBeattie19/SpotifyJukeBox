from pprint import pprint

pprint(JSONReader.read("database.json"))




''' 
from flask import Flask, escape, request 


app = Flask(__name__) 


@app.route('/')
def hello():
    name = request.args.get("name", "World") 
    return f'hello {escape(name)}!' 
'''
