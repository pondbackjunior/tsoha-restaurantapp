from db import db
import users
from sqlalchemy.sql import text

def create(name, type):
    sql = text(f"INSERT INTO {type} (name) VALUES (:name)")
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return True

def remove_category(deleted_categories, deleted_types):
    for category_id in deleted_categories:
        #First delete restaurants_categories assignments
        sql = text("DELETE FROM restaurants_categories WHERE category_id=:category_id")
        db.session.execute(sql, {"category_id":category_id})

        #Then delete the category itself
        sql = text("DELETE FROM categories WHERE id=:category_id")
        db.session.execute(sql, {"category_id":category_id})

    for type_id in deleted_types:
        sql = text("DELETE FROM restaurants_types WHERE type_id=:type_id")
        db.session.execute(sql, {"type_id":type_id})

        sql = text("DELETE FROM types WHERE id=:type_id")
        db.session.execute(sql, {"type_id":type_id})

    db.session.commit()
    return True

def get_category_list():
    sql = text(f"SELECT id, name FROM categories ORDER BY name ASC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_type_list():
    sql = text(f"SELECT id, name FROM types ORDER BY name ASC")
    result = db.session.execute(sql)
    return result.fetchall()

# For restaurant.html
def get_categories_for_restaurant(res_id):
    sql = text(f"SELECT C.id, C.name FROM categories C, restaurants_categories RC WHERE C.id=RC.category_id AND RC.restaurant_id=:res_id ORDER BY name ASC")
    result = db.session.execute(sql, {"res_id":res_id})
    return result.fetchall()

# For restaurant.html
def get_types_for_restaurant(res_id):
    sql = text(f"SELECT T.id, T.name FROM types T, restaurants_types RT WHERE T.id=RT.type_id AND RT.restaurant_id=:res_id ORDER BY name ASC")
    result = db.session.execute(sql, {"res_id":res_id})
    return result.fetchall()

#For add_categories.html
def get_assigned_categories(res_id):
    sql = text("SELECT category_id FROM restaurants_categories WHERE restaurant_id = :res_id")
    result = db.session.execute(sql, {"res_id": res_id})
    return [row[0] for row in result.fetchall()]

#For add_categories.html
def get_assigned_types(res_id):
    sql = text("SELECT type_id FROM restaurants_types WHERE restaurant_id = :res_id")
    result = db.session.execute(sql, {"res_id": res_id})
    return [row[0] for row in result.fetchall()]

def add_categories(res_id, added_categories, added_types):
    for category_id in added_categories:
        sql = text("INSERT INTO restaurants_categories (restaurant_id, category_id) VALUES (:restaurant_id, :category_id)")
        db.session.execute(sql, {"restaurant_id":res_id, "category_id":category_id})

    for type_id in added_types:
        sql = text("INSERT INTO restaurants_types (restaurant_id, type_id) VALUES (:restaurant_id, :type_id)")
        db.session.execute(sql, {"restaurant_id":res_id, "type_id":type_id})

    db.session.commit()
    return True

def delete_categories(res_id, deleted_categories, deleted_types):
    for category_id in deleted_categories:
        sql = text("DELETE FROM restaurants_categories WHERE restaurant_id=:restaurant_id AND category_id=:category_id")
        db.session.execute(sql, {"restaurant_id":res_id, "category_id":category_id})

    for type_id in deleted_types:
        sql = text("DELETE FROM restaurants_types WHERE restaurant_id=:restaurant_id AND type_id=:type_id")
        db.session.execute(sql, {"restaurant_id":res_id, "type_id":type_id})

    db.session.commit()
    return True