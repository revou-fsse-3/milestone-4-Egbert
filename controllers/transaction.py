from flask import Blueprint, render_template, request,jsonify
from connectors.mysql_connector import engine
from models.transaction import Transaction
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import current_user, login_required
from decorators.role_checker import role_required
from validations.transaction_schema import transaction_schema
from cerberus import Validator

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/transactions', methods=['GET'])
# @login_required
def transaction_home():
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try :
        transaction_query = select(Transaction)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            transaction_query = transaction_query.where(or_(Transaction.from_transaction_id.like(f"%{search_query}%"), Transaction.to_transaction_id.like(f"%{search_query}%"), Transaction.type.like(f"%{search_query}%"), Transaction.description.like(f"%{search_query}%")))

        transactions = session.execute(transaction_query)
        transactions = transactions.scalars()
        response_data['transactions'] = transactions
    except Exception as e:
        print(e)
        return"Error Processing Data"

    return render_template("transactions/transaction_home.html", response_data = response_data)

@transaction_routes.route("/transactions/<id>", methods=['GET'])
# @role_required('admin')
def transaction_detail(id):
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        transaction = session.query(Transaction).filter((Transaction.id==id)).first()
        if (transaction == None):
            return "Data not found"
        response_data['transaction'] = transaction
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("transactions/transaction_detail.html", response_data = response_data)

@transaction_routes.route("/transactions", methods=['POST'])
# @role_required('admin')
def transaction_insert():

    v = Validator(transaction_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400
    
    new_transaction = Transaction(
        from_account_id = json_data["from_account_id"],
        to_account_id = json_data['to_account_id'],
        amount =  json_data['amount'],
        type = json_data['type'],
        description = json_data['description']
    )

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        session.add(new_transaction)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to insert data"}

    return { "message": "Success insert data"}

@transaction_routes.route("/transactions/<id>", methods=['PUT'])
@role_required('admin')
def transaction_update(id):

    v = Validator(transaction_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        return jsonify({"error": v.errors}), 400

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        transaction = session.query(Transaction).filter(Transaction.id==id).first()

        transaction.from_account_id = json_data['from_account_id']
        transaction.to_account_id = json_data['to_account_id']
        transaction.amount = json_data['amount']
        transaction.type = json_data['type']
        transaction.description = json_data['description']
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to Update data"}
    
    return { "message": "Success updating data"}

@transaction_routes.route("/transactions/<id>", methods=['DELETE'])
@role_required('admin')
def transaction_delete(id):

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        transaction = session.query(Transaction).filter(Transaction.id==id).first()
        session.delete(transaction)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Fail to delete data"}
    
    return { "message": "Success delete data"}