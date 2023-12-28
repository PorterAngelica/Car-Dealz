#routes("/")
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session
from flask_app.models import login_reg_model
from flask_app.models.login_reg_model import User
from flask_app.models.car_model import Car

#visible routes


@app.route('/new')
def add_car():
    data = {
        "id": session["user.id"]
    }
    car = Car.save(data)
    return render_template("add_car.html", user = login_reg_model.User.get_one_user_by_id(data), car = car)


@app.route('/cars/<int:id>')
def view_car(id):
    data = {
        'id': id
    }
    user_data = {
        "id": session["user.id"]
    }
    return render_template('view_car.html',car = Car.get_by_id(data), user =login_reg_model.User.get_one_user_by_id(user_data))


@app.route('/car/delete/<car_id>')
def delete(car_id):
    Car.delete(car_id)# - we need to be able to call our method from our model 
    return redirect('/dashboard')


@app.route('/car/edit/<int:id>')
def edit_car(id):
    return render_template('edit_car.html',car = Car.get_by_id({'id': id}))


#hidden routes


@app.route('/add_car_to_db', methods=["POST"])
def add_car_to_db():
    if not Car.validate_form(request.form):
        return redirect('/new')
    Car.save(request.form)
    return redirect('/dashboard')


@app.route('/car/edit/process/<int:id>', methods=['POST'])
def process_edit_car(id):
    if not Car.validate_form(request.form):
        return redirect(f'/car/edit/{id}')

    data = {
        'id': id,
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
    }
    Car.update(data)
    return redirect('/dashboard')