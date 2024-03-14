from flask import Blueprint, render_template
from connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from models.account import Account

account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/accounts', methods=['GET'])
def account_home():
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try :
        account_query = select(Account)
        accounts = session.execute(account_query)
        accounts = accounts.scalars()
        response_data['accounts'] = accounts
        
    except Exception as e:
        print(e)
        return"Error Processing Data"
    return render_template("accounts/index.html", response_data = response_data)

# @account_routes.route('/accounts', methods=['POST'])
# def account_insert():
#     new_account = Account(

#     )