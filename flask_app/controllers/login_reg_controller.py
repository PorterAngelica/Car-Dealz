#routes("/")
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session
from flask_app.models import login_reg_model
from flask_app.models.login_reg_model import User
from flask_app.models.car_model import Car
# from flask_app.models import recipes_model

#visible routes

@app.route('/')
def index():
    return render_template("login_reg.html")

@app.route('/dashboard')
def dashboard():
    data = {
        "id": session["user.id"]
    }
    # print(session['user.id'])
    all_cars = Car.get_all()
    return render_template("dashboard.html", user = login_reg_model.User.get_one_user_by_id(data), car = all_cars)



#hidden routes 

@app.route('/login', methods=["POST"])
def login():
    if not login_reg_model.User.validate_login(request.form):
        return redirect('/')
    email_data = {
        "email": request.form["email"]
    }
    found_user = login_reg_model.User.get_user_by_email(email_data)
    session['user.id'] = found_user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    if not login_reg_model.User.validate_registration(request.form):
        return redirect('/')
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":bcrypt.generate_password_hash(request.form["password"])
    }

    session["user.id"] = login_reg_model.User.register_user(user_data)
    return redirect('/dashboard')
