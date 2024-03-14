from flask import Flask
from connectors.mysql_connector import connection
from controllers.account import account_routes

app=Flask(__name__)
app.register_blueprint(account_routes)

@app.route('/')
def home():
    return "Welcome to the Home Page!"