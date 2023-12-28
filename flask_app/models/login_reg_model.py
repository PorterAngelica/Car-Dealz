from flask_app.config.mysqlconnection import connectToMySQL
# from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import bcrypt
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    db_name ="car_deal_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.contents = []

    @classmethod
    def register_user(cls,data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s,%(last_name)s,%(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_one_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return  cls(results[0])
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            found_user =  cls(results[0])
            return found_user



    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            is_valid = False
            flash("first name must be two or more characters", "registration")

        if len(data["last_name"]) < 2:
            is_valid = False
            flash("last name must be two or more characters", "registration")

        #validation for email
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Email is not correctly formatted", "registration")

            #validation for unique email

            #validate for an existent email
        found_user_or_none = User.get_user_by_email({"email": data["email"]})
        if found_user_or_none != None:
            is_valid = False
            flash("Email is already taken", "registration")


            #check wether the password is long enough
        if len(data["password"]) < 8:
            is_valid = False
            flash("password must be at least 8 characters", "registration")

        if data["password"] != data["confirm_password"]:
            is_valid = False
            flash("passwords do not match", "registration")
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        found_user_or_none = User.get_user_by_email({"email": form_data["email"]})
        if found_user_or_none == None:
            is_valid = False
            flash("Invalid Login Credentials", "login")

        elif not bcrypt.check_password_hash(found_user_or_none.password, form_data["password"]):
            is_valid = False
            flash("Invalid Login Credentials", "login")
        return is_valid
