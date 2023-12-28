from flask_app import app
from flask_app.controllers import login_reg_controller
from flask_app.controllers import car_controller

if __name__=="__main__":

    app.run(debug=True)