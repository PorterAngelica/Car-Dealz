from flask_app.config.mysqlconnection import connectToMySQL
# from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import bcrypt
from flask_app.models.login_reg_model import User
from flask_app.models import login_reg_model
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Car:

    db_name ="car_deal_schema"

    def __init__(self,data):
        self.user = [data.get('user') or None]
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO cars (price, model, make, year, description , users_id)
        VALUES
        (%(price)s , %(model)s, %(make)s, %(year)s,%(description)s, %(users_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls,car_id):
        query = """
        DELETE FROM cars where id = %(id)s;
        """
        connectToMySQL(cls.db_name).query_db(query,{"id": car_id})
        return car_id


    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM cars
        JOIN users on cars.users_id = users.id;
        """
        results = connectToMySQL(cls.db_name).query_db(query)

        # print("raw data for all posts", results)

        all_car = []
        #iterate over the raw data list of post dictionaries
        for row in results:
        #each loop #
        # - make user instance
            posting_user = User({
                "id": row["users_id"],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            })
        #make post instance with user object
            new_post = Car({
                "id": row['id'],
                "price": row['price'],
                "model": row['model'],
                "make": row['make'],
                "year": row['year'],
                "description": row['description'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "users_id": row["users_id"],
                "user": posting_user,
            })
        #add post to all_posts list
            all_car.append(new_post)
        return all_car
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM cars
                JOIN users on cars.users_id = users.id
                WHERE cars.id = %(id)s;
                """
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE cars
                SET price = %(price)s,
                model = %(model)s,
                make = %(make)s ,
                year = %(year)s,
                description = %(description)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db_name).query_db(query,form_data)
    
    @staticmethod
    def validate_form(car):
        is_valid = True
        if len(car["price"]) <= 0:
            is_valid = False
            flash("price must be grater than 0", "car")

        if len(car["model"]) == 0:
            is_valid = False
            flash("Model field is required", "car")

        if len(car["make"]) == 0:
            is_valid = False
            flash("make field is required", "car")

        if len(car["year"])  <= 0:
            is_valid = False
            flash("year must be grater than 0", "car")

        if len(car["description"]) == 0 :
            is_valid = False
            flash("Description field is required", "car")
        return is_valid
    





