from flask import Blueprint, render_template, request, redirect
from connectors.mysql_connector import engine
from models.user import User
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, login_required, current_user

user_routes = Blueprint('user_routes',__name__)

@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")

@user_routes.route("/users", methods=['POST'])
def do_user_registration():

    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password']
    role = request.form['role']
    NewUser = User(username=username, email=email, role=role)
    NewUser.set_password(password_hash)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        session.add(NewUser)
        session.commit()
    except Exception as e:
        session.rollback()
        return {"message": "Gagal Register"}

    return {"message": "Sukses Register"}

@user_routes.route("/users/me", methods=["GET"])
@login_required
def detail_profile():
    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        response_data['username'] = current_user.username
        response_data['email'] = current_user.email
        response_data['role'] = current_user.role
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("users/detail_user.html", response_data = response_data)

# @user_routes.route("/user/me", methods=['PUT'])
# def user_update():

#     connection = engine.connect()
#     Session = sessionmaker(connection)
#     session = Session()
#     session.begin()

#     try:
#         # Get data from request body
#         # username = request.json.get('username', current_user.username)
#         # password = request.json.get('password')
#         # new_password = request.json.get('new_password')
#         # email = request.json.get('email', current_user.email)

#         # if username != current_user.username:
#         #     user = User.query.filter_by(username=username).first()
#         #     if user is not None:
#         #         raise ValueError("Username already exists")
        
#         # # Update profile information
#         # current_user.username = username
#         # if password is not None and new_password is not None:
#         #     if not bcrypt_sha256.verify(password, current_user.password):
#         #         raise ValueError("Current password does not match")
            
#         #     current_user.set_password(new_password)
#         # else:
#         #     current_user.email = email
    
#         # # Commit the changes to the database
#         # session.add(current_user)
#         # session.commit()
#     # except Exception as e:
#     #     print(e)
#     #     session.rollback()
#     #     return jsonify({'error': str(e)}), 400
#         user = session.query(User).filter(User.id==current_user.id).first()

#         user.username = request.form['username']
#         user.email = request.form['email']
#         user.password_hash = request.form['password_hash']
#         account.role = request.form['role']

#         session.commit()
#     except Exception as e:
#         session.rollback()
#         return { "message": "Fail to Update data"}
    
#     return { "message": "Success updating data"}

@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    try:
        user = session.query(User).filter(User.email==request.form['email']).first()

        if user == None:
            return {"message": "Email tidak terdaftar"}
            
        if not user.check_password(request.form['password']):
            return {"message": "Password salah"}
            
        login_user(user, remember=False)
        return redirect('/accounts')
    except Exception as e:
        return {"message": "Gagal Login"}

@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/login')

