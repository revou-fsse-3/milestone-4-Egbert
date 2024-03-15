from dotenv import load_dotenv
from flask import Flask
from connectors.mysql_connector import engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from models.account import Account
from sqlalchemy import select
from flask_login import LoginManager
from models.user import User
import os
from controllers.account import account_routes
from controllers.user import user_routes

load_dotenv()


app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(account_routes)
app.register_blueprint(user_routes)

@app.route('/')
def home():
    connection = engine.connect()
    account_query = select(Account)
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(account_query)
        for row in result.scalars():
            print(f'ID: {row.id}, User_ID: {row.user_id}, Account_Type: {row.account_type}')

    return "<p>Insert Success</p>"