from db import db
import users
from sqlalchemy.sql import text
import datetime

def get_list(order_by):
    sql = text(f"SELECT R.name, R.description, R.opening_time, R.closing_time, COALESCE(AVG(RR.rating),0) AS rating, R.id as newest FROM restaurants R \
               LEFT JOIN restaurants_ratings RR ON R.id=RR.restaurant_id GROUP BY R.id \
               ORDER BY {order_by} DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_details(restaurant_name):
    sql = text("SELECT name, description, opening_time, closing_time, id FROM restaurants WHERE name=:name")
    result = db.session.execute(sql, {"name":restaurant_name.replace("_", " ")})
    res = result.fetchall()
    if res:
        return res
    else:
        return None

def get_avg_rating(restaurant_name):
    id = restaurant_id_from_name(restaurant_name)
    sql = text("SELECT AVG(RR.rating) FROM restaurants_ratings RR, restaurants R WHERE RR.restaurant_id=R.id AND R.id=:id")
    result = db.session.execute(sql, {"id":id})
    res = result.fetchone()[0]
    if res:
        return res
    else:
        return 0

def create(name, description, opening_time, closing_time):
    sql = text("INSERT INTO restaurants (name, description, opening_time, closing_time) VALUES (:name, :description, :opening_time, :closing_time)")
    db.session.execute(sql, {"name":name, "description":description, "opening_time":opening_time, "closing_time":closing_time})
    db.session.commit()
    return True

def restaurant_id_from_name(name):
    sql = text("SELECT R.id FROM restaurants R WHERE name = :name")
    result = db.session.execute(sql, {"name":name})
    res = result.fetchone()
    if res:
        return res[0]
    else:
        return None

def comment(comment, rating, restaurant_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    restaurant_id = restaurant_id_from_name(restaurant_name)
    sql = text("INSERT INTO restaurants_ratings (comment, rating, user_id, restaurant_id, sent_at) VALUES (:comment, :rating, :user_id, :restaurant_id, NOW())")
    db.session.execute(sql, {"comment":comment, "rating":rating, "user_id":user_id, "restaurant_id":restaurant_id})
    db.session.commit()
    return True

def get_comment_list(res_name):
    sql = text("SELECT RR.comment, RR.rating, U.username, RR.restaurant_id, RR.sent_at, RR.id FROM users U, restaurants_ratings RR, restaurants R \
               WHERE U.id=RR.user_id AND RR.restaurant_id=R.id AND R.name=:res_name ORDER BY RR.sent_at DESC")
    result = db.session.execute(sql, {"res_name":res_name})
    return result.fetchall()

def delete_comment(comment_id):
    sql = text(f"DELETE FROM restaurants_ratings WHERE id={comment_id}")
    db.session.execute(sql)
    db.session.commit()
    return True

def delete_restaurant(res_id):
    sql = text(f"DELETE FROM restaurants WHERE id={res_id}")
    db.session.execute(sql)
    db.session.commit()
    return True

def edit_restaurant(name, description, opening_time, closing_time, res_id):
    sql = text(f"UPDATE restaurants SET name=:name, description=:description, opening_time=:opening_time, closing_time=:closing_time WHERE id={res_id}")
    db.session.execute(sql, {"name":name, "description":description, "opening_time":opening_time, "closing_time":closing_time})
    db.session.commit()
    return True

def get_today_weekday():
    today = datetime.datetime.today()
    weekday_name = today.strftime('%A')
    return weekday_name
