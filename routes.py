from app import app
from flask import render_template, request, redirect
import users, restaurants, categories
from db import db
from sqlalchemy.sql import text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        users.generate_default_admin()
        today = restaurants.get_today_weekday()
        try:
            order_by = request.args.get("order_by", "newest")
            restaurant_list = restaurants.get_list(order_by)
        except Exception as e:
            print(e) 
            order_by = "newest"
            restaurant_list = restaurants.get_list(order_by)
        return render_template("index.html", order_by=order_by, count=len(restaurant_list), restaurants=restaurant_list, today=today)
    if request.method == "POST":
        order_by = request.form["order_by"]
        return redirect(f"/?order_by={order_by}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        
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
        name = request.form["name"]
        description = request.form["description"]
        opening_time = request.form["opening_time"]
        closing_time = request.form["closing_time"]
        if restaurants.create(name, description, opening_time, closing_time):
            return redirect("/")
        else:
            return render_template("error.html", message="Luominen ei onnistunut")

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
        res_name = restaurants.get_details(restaurant_name)[0][0]
        res_desc = restaurants.get_details(restaurant_name)[0][1]
        res_op = restaurants.get_details(restaurant_name)[0][2]
        res_cl = restaurants.get_details(restaurant_name)[0][3]
        res_rat = f"{restaurants.get_avg_rating(restaurant_name):.2f}"
        res_id = restaurants.get_details(restaurant_name)[0][4]
        category_list = categories.get_categories_for_restaurant(res_id)
        type_list = categories.get_types_for_restaurant(res_id)
        comment_list = restaurants.get_comment_list(res_name)
        if res_name:
            return render_template("restaurant.html", res_name=res_name, res_desc=res_desc, res_op=res_op, res_cl=res_cl, res_rat=res_rat,
                                   count=len(comment_list), comments=comment_list, categories=category_list, types=type_list)
        else:
            return "Ravintolaa ei löytynyt", 404
    if request.method == "POST":
        comment = request.form["comment"]
        rating = request.form["rating"]
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
    res_name = restaurants.get_details(restaurant_name)[0][0]
    res_id = restaurants.get_details(restaurant_name)[0][4]
    if request.method == "GET":
        return render_template("delete_restaurant.html", res_name=res_name)
    if request.method == "POST":
        if restaurants.delete_restaurant(res_id):
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
    res_name = restaurants.get_details(restaurant_name)[0][0]
    res_id = restaurants.get_details(restaurant_name)[0][4]
    if request.method == "GET":
        return render_template("edit_restaurant.html", res_name=res_name)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        opening_time = request.form["opening_time"]
        closing_time = request.form["closing_time"]
        if restaurants.edit_restaurant(name, description, opening_time, closing_time, res_id):
            return redirect(f"/restaurant/{name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Muokkaaminen ei onnistunut")
        
@app.route("/restaurant/<restaurant_name>/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(restaurant_name, comment_id):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    res_name = restaurants.get_details(restaurant_name)[0][0]
    if request.method == "GET":
        return render_template("delete_comment.html", comment_id=comment_id, res_name=res_name)
    if request.method == "POST":
        if restaurants.delete_comment(comment_id):
            return redirect(f"/restaurant/{res_name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Poistaminen ei onnistunut")
        
@app.route("/add_categories/<restaurant_name>", methods=["GET", "POST"])
def add_categories(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    category_list = categories.get_category_list()
    type_list = categories.get_type_list()
    res_name = restaurants.get_details(restaurant_name)[0][0]
    res_id = restaurants.get_details(restaurant_name)[0][4]

    # Get assigned categories and types
    assigned_categories = categories.get_assigned_categories(res_id)
    assigned_types = categories.get_assigned_types(res_id)

    # Filter out assigned categories and types
    categories_to_add = [category for category in category_list if category[0] not in assigned_categories]
    types_to_add = [type for type in type_list if type[0] not in assigned_types]

    if request.method == "GET":
        return render_template("add_categories.html", res_name=res_name, res_id=res_id, categories=categories_to_add, types=types_to_add)
    if request.method == "POST":
        added_categories = request.form.getlist("categories[]")
        added_types = request.form.getlist("types[]")
        if categories.add_categories(res_id, added_categories, added_types):
            return redirect(f"/restaurant/{res_name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Muokkaaminen ei onnistunut")
        
@app.route("/delete_categories/<restaurant_name>", methods=["GET", "POST"])
def delete_categories(restaurant_name):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    res_name = restaurants.get_details(restaurant_name)[0][0]
    res_id = restaurants.get_details(restaurant_name)[0][4]

    # Get assigned categories and types
    assigned_categories = categories.get_categories_for_restaurant(res_id)
    assigned_types = categories.get_types_for_restaurant(res_id)

    if request.method == "GET":
        return render_template("delete_restaurant_categories.html", res_name=res_name, res_id=res_id, categories=assigned_categories, types=assigned_types)
    if request.method == "POST":
        deleted_categories = request.form.getlist("categories[]")
        deleted_types = request.form.getlist("types[]")
        if categories.delete_categories(res_id, deleted_categories, deleted_types):
            return redirect(f"/restaurant/{res_name.replace(' ', '_')}")
        else:
            return render_template("error.html", message="Muokkaaminen ei onnistunut")