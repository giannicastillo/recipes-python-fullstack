
from unicodedata import name
from flask_app import app
from flask import render_template, redirect, request, session,flash

from flask_app.models.owner import Owner
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template ("index.html")

#==========================================
#Register / Login Routes
#============================================

@app.route("/register" , methods=["POST"])
def register():
    #1 validating form information
    data={
        "first_name" : request.form["first_name"], 
        "last_name" : request.form["last_name"], 
        "email" : request.form["email"], 
        "password" : request.form["password"], 
        "pass_conf" : request.form["pass_conf"]
    }
    
    if not Owner.validate_register(data):
        return redirect("/")


    #2 - bcrypt password
    data["password"] = bcrypt.generate_password_hash(request.form['password'])


    #3 - save new owner to db 

    new_owner_id = Owner.create_owner(data)

    #4 enter owner into session and redirect into dashboard
    session["owner_id"] = new_owner_id
    return redirect("/dashboard")
#========================
#LOGIN METHODS BELOW 
#=========================
@app.route("/login", methods=["POST"])
def login():
    #1 validate login info 
    data ={
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not Owner.validate_login(data):
        return redirect("/")

    #2 query for owner info based on email 

    owner = Owner.get_by_email(data)


    #3 put owner id into session and redirect into dashboard

    session["owner_id"] = owner.id
    return redirect("/dashboard")

#===============================
# RENDER DASHBOARD ROUTE
#================================

@app.route("/dashboard")
def dashboard():
    if "owner_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")
#==========================================
# SYNC INFO TO DATABASE IN THE SAME ROUTE 
#===========================================
    data = {
        "id" : session["owner_id"]
    }

    owner = Owner.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template("dashboard.html", owner = owner, all_recipes = all_recipes)



#===============================
# LOGOUT ROUTE
#================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect('/')

#==================================
#ROUTE CREATE BOTTOM FROM DASH TO CREATE PAGE
#================================
@app.route("/recipes/new")
def go_to_create():
    return render_template('create.html')



#=====================================================
#POST INFO TO DATABASE AND REDIRECT POST BACK TO DASHBOARD
#======================================================
@app.route("/recipes/new", methods = ['POST'])
def add_recipe():
    #create_recipe

    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instruction" : request.form["instruction"],
        "owner_id" : session["owner_id"],
        "created_at" : session["created_at"]
    }

    new_recipe = Recipe.create_recipe(data)
    return redirect (f'/dashboard')

#==============================
##ROUTE FROM DASHBOARD TO EDIT PG 
#==============================

@app.route('/recipes/edit/<int:id>')
def edit_page(id):
    data = {
        "id": id,
    }
    recipe=Recipe.show_user(data)
    return render_template('edit.html', recipe = recipe)
#=======================
#REDIRECT TO DASHBOARD AFTER UPDATE
#========================
@app.route('/recipes/edit',methods=["POST"])
def recipe_edit():
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instruction" : request.form["instruction"],
        "owner_id" : session["owner_id"],
        "id" : request.form["recipe_id"]
    }

    print(data)
    Recipe.edit_recipe(data)
    return redirect (f'/dashboard')


#==============================
# ROUTE TO SHOWPAGE.HTML FROM "VIEW INSTRUCTIONS"
#=============================
@app.route('/recipes/<int:id>')
def goto_showpage(id):
    data = {
        "id": id
    }
    thisowner = {
        "id" : session['owner_id']
    }
    owner= Owner.get_by_id(thisowner)
    recipe = Recipe.one_recipe(data)
    return render_template('showpage.html', recipe= recipe, owner = owner)


#=================================
# DELETE RECIPE // NEED HELP! 
#=================================

@app.route('/delete/<int:recipe_id>')
def remove_recipe(recipe_id):
    data={
        "recipe_id" : recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')