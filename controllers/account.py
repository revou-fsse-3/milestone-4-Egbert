from flask import Blueprint, render_template, request,jsonify
from connectors.mysql_connector import engine
from models.account import Account
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required
from decorators.role_checker import role_required
from validations.account_schema import account_schema
from cerberus import Validator

account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/accounts', methods=['GET'])
@login_required
def account_home():
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try :
        account_query = select(Account)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            account_query = account_query.where(or_(Account.user_id.like(f"%{search_query}%"), Account.account_type.like(f"%{search_query}%"), Account.account_number.like(f"%{search_query}%")))

        accounts = session.execute(account_query)
        accounts = accounts.scalars()
        response_data['accounts'] = accounts
        response_data['username'] = current_user.username
        response_data['role'] = current_user.role
        
    except Exception as e:
        print(e)
        return"Error Processing Data"

    return render_template("accounts/account_home.html", response_data = response_data)

@account_routes.route("/accounts/<id>", methods=['GET'])
@role_required('admin')
def account_detail(id):
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        account = session.query(Account).filter((Account.id==id)).first()
        if (account == None):
            return "Data not found"
        response_data['account'] = account
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("accounts/account_detail.html", response_data = response_data)

@account_routes.route("/accounts", methods=['POST'])
def account_insert():

    v = Validator(account_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    
    new_account = Account(
        user_id = json_data["user_id"],
        account_type = json_data['account_type'],
        account_number=  json_data['account_number'],
        balance = json_data['balance']
    )

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        session.add(new_account)
        session.commit()
    except Exception as e:
        session.rollback()
        return { "message": "Fail to insert data"}

    return { "message": "Success insert data"}

@account_routes.route("/accounts/<id>", methods=['DELETE'])
@role_required('admin')
def account_delete(id):

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        account = session.query(Account).filter(Account.id==id).first()
        session.delete(account)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to delete data"}
    
    return { "message": "Success delete data"}

@account_routes.route("/accounts/<id>", methods=['PUT'])
@role_required('admin')
def account_update(id):

    v = Validator(account_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        account = session.query(Account).filter(Account.id==id).first()

        account.user_id = json_data['user_id']
        account.account_type = json_data['account_type']
        account.account_number = json_data['account_number']
        account.balance = json_data['balance']
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to Update data"}
    
    return { "message": "Success updating data"}