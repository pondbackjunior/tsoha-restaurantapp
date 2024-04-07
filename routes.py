from app import app
from flask import render_template, request, redirect
import users, restaurants

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        users.generate_default_admin()
        try:
            order_by = request.args.get("order_by", "newest")
            restaurant_list = restaurants.get_list(order_by)
        except Exception as e:
            print(e) 
            order_by = "newest"
            restaurant_list = restaurants.get_list(order_by)
        return render_template("index.html", order_by=order_by, count=len(restaurant_list), restaurants=restaurant_list)
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

@app.route("/create", methods=["GET", "POST"])
def create():
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

@app.route("/restaurant/<restaurant_name>", methods=["GET", "POST"])
def restaurant(restaurant_name):
    if request.method == "GET":
        res_name = restaurants.get_details(restaurant_name)[0][0]
        res_desc = restaurants.get_details(restaurant_name)[0][1]
        res_op = restaurants.get_details(restaurant_name)[0][2]
        res_cl = restaurants.get_details(restaurant_name)[0][3]
        res_rat = f"{restaurants.get_avg_rating(restaurant_name):.2f}"
        list = restaurants.get_comment_list(res_name)
        if res_name:
            return render_template("restaurant.html", res_name=res_name, res_desc=res_desc, res_op=res_op, res_cl=res_cl, res_rat=res_rat, count=len(list), comments=list)
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
        
@app.route("/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    if users.user_role() != "admin" or users.user_id() == 0:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")
    if request.method == "GET":
        return render_template("delete_comment.html", comment_id=comment_id)
    if request.method == "POST":
        if restaurants.delete_comment(comment_id):
            return redirect("/")
        else:
            return render_template("error.html", message="Poistaminen ei onnistunut")