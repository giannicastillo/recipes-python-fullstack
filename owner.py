
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import dog
from flask import flash

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Owner:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_register(data):
        is_valid = True

        if len(data["first_name"]) < 2: 
            flash("First Name must be at least 2 characters long!")
            is_valid = False

        if len(data["last_name"]) < 2: 
            flash("Last Name must be at least 2 characters long!")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash ("Invalid Email!")
            is_valid = False
        
        if Owner.get_by_email(data):
            flash("Email already in use! Please registernew email or login!")
            is_valid = False

        if len(data["password"]) < 5: 
            flash("Password must be at least 5 characters long!")
            is_valid = False
        if data["password"]!= data["pass_conf"]:
            flash("Password and Password Confirmation must match!")
            is_valid = False
        return is_valid
            
    @staticmethod
    def validate_login(data):
        is_valid = True

        owner_in_db = Owner.get_by_email(data)
        # user is not registered in the db
        if not owner_in_db:
            flash("Invalid Credentials")
            is_valid = False
        elif not bcrypt.check_password_hash(owner_in_db.password, data["password"]):
            # if we get False after checking the password
            flash("Invalid Credentials")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM owners WHERE id = %(id)s;"
        result = connectToMySQL("owners_recipes_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM owners WHERE email = %(email)s;"
        result = connectToMySQL("owners_recipes_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_owner(cls, data):
        query= "INSERT INTO owners (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        results= connectToMySQL("owners_recipes_schema").query_db(query, data)
        return results

