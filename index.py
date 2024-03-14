from flask import Flask
from connectors.mysql_connector import connection

app=Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"