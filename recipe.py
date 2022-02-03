from tkinter import INSERT
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import owner

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = []

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN owners on recipes.owner_id = owners.id;"
        results= connectToMySQL("owners_recipes_schema").query_db(query)
        all_recipes= []
        for row in results:
            recipe = cls(row)
            owner_data = {
                "id" : row['id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
            }
            recipe.owner = owner.Owner(owner_data)
            all_recipes.append (recipe)
        return all_recipes

    @classmethod
    def create_recipe(cls, data):
        query= "INSERT INTO recipes (name, description, instruction, owner_id, created_at, updated_at)VALUES (%(name)s, %(description)s, %(instruction)s , %(owner_id)s, NOW(), NOW());"
        new_recipe= connectToMySQL("owners_recipes_schema").query_db(query,data)
        return new_recipe

    @staticmethod
    def validate_register(data):
        is_valid = True

        if len(data["name"]) < 3: 
            flash("Recipe must be at least 2 characters long!")
            is_valid = False
        if len(data["description"]) < 3: 
            flash("Description must be at least 2 characters long!")
            is_valid = False
        if len(data["instruction"]) < 3: 
            flash("Instructions must be at least 2 characters long!")
            is_valid = False
        return is_valid

    @classmethod
    def show_user(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL('owners_recipes_schema').query_db(query,data)
        return cls(results[0])

    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name =%(name)s , description = %(description)s, instruction =%(instruction)s, owner_id= %(owner_id)s, created_at = NOW() WHERE id= %(id)s;"
        results = connectToMySQL('owners_recipes_schema').query_db(query,data)
        return results

    @classmethod
    def one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('owners_recipes_schema').query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def delete_recipe(cls,data):
        query= "DELETE FROM recipes WHERE id=%(recipe_id)s;"
        return connectToMySQL('owners_recipes_schema').query_db(query,data)
        