from app import app
from flask import render_template, request, redirect, jsonify
import users, restaurants, categories
from db import db
from sqlalchemy.sql import text
from os import getenv

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        api_key = getenv("API_KEY") # Needs Google Maps API key to function.
        today = restaurants.get_today_weekday()
        try:
            order_by = request.args.get("order_by", "newest")
            restaurant_list = restaurants.get_list(order_by)
        except:
            order_by = "newest"
            restaurant_list = restaurants.get_list(order_by)
        return render_template("index.html", order_by=order_by, count=len(restaurants.get_list(order_by, limit=9999)), restaurants=restaurant_list, today=today, api_key=api_key)
    if request.method == "POST":
        order_by = request.form["order_by"]
        return redirect(f"/?order_by={order_by}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error=True)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=None)
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", error="Salasanat eivät täsmää.")
        if len(username) < 3 or len(username) > 20:
            return render_template("register.html", error="Käyttäjänimi on väärän pituinen.")
        if len(password1) < 6 or len(password1) > 30:
            return render_template("register.html", error="Salasana on väärän pituinen.")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error="Käyttäjänimi on varattu.")
        
@app.route("/result")
def result():
    query = request.args["query"]
    sql = text("SELECT id, name, description FROM restaurants WHERE description ILIKE :query OR name ILIKE :query ORDER BY name ASC")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    restaurants = result.fetchall()
    return render_template("result.html", restaurants=restaurants)

@app.route("/create_restaurant", methods=["GET", "POST"])
def create_restaurant():
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    if request.method == "GET":
        return render_template("new_restaurant.html")
    if request.method == "POST":
        try:
            name = request.form["name"]
            description = request.form["description"]
            address = request.form["address"]
            coord_x = float(request.form["coord_x"])
            coord_y = float(request.form["coord_y"])
            is_24h = request.form["is_24h"]
            # Initialize dictionaries for open/close times
            opening_times = {}
            
            # Retrieve form inputs for opening and closing times, handle empty values
            for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                open_time = request.form.get(f"open_{day}")
                close_time = request.form.get(f"close_{day}")
                
                # Only add times to the dictionary if they're not empty
                if open_time:
                    opening_times[f"open_{day}"] = open_time
                if close_time:
                    opening_times[f"close_{day}"] = close_time
            if restaurants.create(name, description, address, coord_x, coord_y, is_24h, **opening_times):
                return redirect("/")
            else:
                return render_template("error.html", message="Luominen ei onnistunut")
        except ValueError:
            # Handle the case where coord_x or coord_y could not be converted to float
            return render_template("error.html", message="Virheelliset koordinaatit, yritä uudelleen.")

@app.route("/create_category", methods=["GET", "POST"])
def create_category():
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    if request.method == "GET":
        return render_template("new_category.html")
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        if categories.create(name, type):
            return redirect("/")
        else:
            return render_template("error.html", message="Luominen ei onnistunut")

@app.route("/restaurant/<restaurant_name>", methods=["GET", "POST"])
def restaurant(restaurant_name):
    if request.method == "GET":
        restaurant = restaurants.get_details(restaurant_name)
        res_rat = f"{restaurants.get_avg_rating(restaurant_name):.2f}"
        category_list = categories.get_categories_for_restaurant(restaurant.id)
        type_list = categories.get_types_for_restaurant(restaurant.id)
        comment_list = restaurants.get_comment_list(restaurant.name)
        today = restaurants.get_today_weekday()
        api_key = getenv("API_KEY")
        if restaurant.name:
            return render_template("restaurant.html", restaurant=restaurant, res_rat=res_rat,
                                   count=len(comment_list), comments=comment_list, categories=category_list,
                                   types=type_list, today=today, api_key=api_key)
        else:
            return "Ravintolaa ei löytynyt", 404
    if request.method == "POST":
        comment = request.form["comment"]
        rating = request.form["rating"]
        if not rating:
            return render_template("error.html", message="Et valinnut arvosanaa.")
        if len(comment) > 5000:
            return render_template("error.html", message="Viesti on liian pitkä")
        if restaurants.comment(comment, rating, restaurant_name):
            return redirect(f"/restaurant/{restaurant_name}")
        else:
            return render_template("error.html", message="Arvostelun lähetys ei onnistunut")
        
@app.route("/delete_restaurant/<restaurant_name>", methods=["GET", "POST"])
def delete_restaurant(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    restaurant = restaurants.get_details(restaurant_name)
    if request.method == "GET":
        return render_template("delete_restaurant.html", res_name=restaurant.name)
    if request.method == "POST":
        if restaurants.delete_restaurant(restaurant.id):
            return redirect("/")
        else:
            return render_template("error.html", message="Poistaminen ei onnistunut")
        
@app.route("/remove_categories", methods=["GET", "POST"])
def remove_categories():
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    
    category_list = categories.get_category_list()
    type_list = categories.get_type_list()

    if request.method == "GET":
        return render_template("remove_categories.html", categories=category_list, types=type_list)
    if request.method == "POST":
        deleted_categories = request.form.getlist("categories[]")
        deleted_types = request.form.getlist("types[]")
        if categories.remove_category(deleted_categories, deleted_types):
            return redirect("/")
        else:
            return render_template("error.html", message="Poistaminen ei onnistunut.")

@app.route("/edit_restaurant/<restaurant_name>", methods=["GET", "POST"])
def edit_restaurant(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    restaurant = restaurants.get_details(restaurant_name)
    if request.method == "GET":
        return render_template("edit_restaurant.html", restaurant=restaurant)
    if request.method == "POST":
        try:
            name = request.form["name"]
            description = request.form["description"]
            address = request.form["address"]
            coord_x = float(request.form["coord_x"])
            coord_y = float(request.form["coord_y"])
            is_24h = request.form["is_24h"]
            # Initialize dictionaries for open/close times
            opening_times = {}
            
            # Retrieve form inputs for opening and closing times, handle empty values
            for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                open_time = request.form.get(f"open_{day}")
                close_time = request.form.get(f"close_{day}")
                
                # Only add times to the dictionary if they're not empty
                if open_time:
                    opening_times[f"open_{day}"] = open_time
                if close_time:
                    opening_times[f"close_{day}"] = close_time
            if restaurants.edit_restaurant(restaurant.id, name, description, address, coord_x, coord_y, is_24h, **opening_times):
                return redirect(f"/restaurant/{name.replace(' ', '_')}")
            else:
                return render_template("error.html", message="Muokkaaminen ei onnistunut")
        except ValueError:
            # Handle the case where coord_x or coord_y could not be converted to float
            return render_template("error.html", message="Virheelliset koordinaatit, yritä uudelleen.")
        
@app.route("/restaurant/<restaurant_name>/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(restaurant_name, comment_id):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    restaurant = restaurants.get_details(restaurant_name)
    if request.method == "GET":
        return render_template("delete_comment.html", comment_id=comment_id, res_name=restaurant.name)
    if request.method == "POST":
        if restaurants.delete_comment(comment_id):
            return redirect(f"/restaurant/{restaurant.name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Poistaminen ei onnistunut")
        
@app.route("/add_categories/<restaurant_name>", methods=["GET", "POST"])
def add_categories(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    category_list = categories.get_category_list()
    type_list = categories.get_type_list()
    restaurant = restaurants.get_details(restaurant_name)

    # Get assigned categories and types
    assigned_categories = categories.get_assigned_categories(restaurant.id)
    assigned_types = categories.get_assigned_types(restaurant.id)

    # Filter out assigned categories and types
    categories_to_add = [category for category in category_list if category[0] not in assigned_categories]
    types_to_add = [type for type in type_list if type[0] not in assigned_types]

    if request.method == "GET":
        return render_template("add_categories.html", res_name=restaurant.name, res_id=restaurant.id, categories=categories_to_add, types=types_to_add)
    if request.method == "POST":
        added_categories = request.form.getlist("categories[]")
        added_types = request.form.getlist("types[]")
        if categories.add_categories(restaurant.id, added_categories, added_types):
            return redirect(f"/restaurant/{restaurant.name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Muokkaaminen ei onnistunut")
        
@app.route("/delete_categories/<restaurant_name>", methods=["GET", "POST"])
def delete_categories(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    restaurant = restaurants.get_details(restaurant_name)

    # Get assigned categories and types
    assigned_categories = categories.get_categories_for_restaurant(restaurant.id)
    assigned_types = categories.get_types_for_restaurant(restaurant.id)

    if request.method == "GET":
        return render_template("delete_restaurant_categories.html", res_name=restaurant.name, res_id=restaurant.id, categories=assigned_categories, types=assigned_types)
    if request.method == "POST":
        deleted_categories = request.form.getlist("categories[]")
        deleted_types = request.form.getlist("types[]")
        if categories.delete_categories(restaurant.id, deleted_categories, deleted_types):
            return redirect(f"/restaurant/{restaurant.name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Muokkaaminen ei onnistunut")

@app.route('/api/restaurants')
def jsonify_restaurants():
    restaurant_list = restaurants.get_dict_list()
    return jsonify(restaurant_list)