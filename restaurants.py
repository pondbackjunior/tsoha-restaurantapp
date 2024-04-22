from db import db
import users
from sqlalchemy.sql import text
import datetime

def get_list(order_by):
    sql = text(f"""SELECT COALESCE(AVG(RR.rating),0) AS rating, R.id as newest,
               R.name, R.description, R.address, R.coord_x, R.coord_y, R.is_24h,
               R.open_mon, R.close_mon, R.open_tue, R.close_tue, R.open_wed, R.close_wed, R.open_thu, R.close_thu,
               R.open_fri, R.close_fri, R.open_sat, R.close_sat, R.open_sun, R.close_sun
               FROM restaurants R
               LEFT JOIN restaurants_ratings RR ON R.id=RR.restaurant_id GROUP BY R.id
               ORDER BY {order_by} DESC""")
    result = db.session.execute(sql)
    return result.fetchall()

def get_dict_list():
    sql = text("SELECT id, name, description, address, coord_x, coord_y FROM restaurants")
    result = db.session.execute(sql)
    
    restaurant_list = [dict(row) for row in result.mappings().all()]
    
    return restaurant_list

def get_details(restaurant_name):
    sql = text("""SELECT id, name, description, address, coord_x, coord_y, is_24h,
               open_mon, close_mon, open_tue, close_tue, open_wed, close_wed, open_thu, close_thu,
               open_fri, close_fri, open_sat, close_sat, open_sun, close_sun FROM restaurants WHERE name=:name""")
    result = db.session.execute(sql, {"name":restaurant_name.replace("_", " ")})
    res = result.fetchall()
    if res:
        return res[0]
    else:
        return None

def get_avg_rating(restaurant_name):
    id = get_details(restaurant_name).id
    sql = text("SELECT AVG(RR.rating) FROM restaurants_ratings RR, restaurants R WHERE RR.restaurant_id=R.id AND R.id=:id")
    result = db.session.execute(sql, {"id":id})
    res = result.fetchone()[0]
    if res:
        return res
    else:
        return 0

def create(name, description, address, coord_x, coord_y, is_24h,
            open_mon=None, close_mon=None, open_tue=None, close_tue=None, open_wed=None, close_wed=None, open_thu=None, close_thu=None,
           open_fri=None, close_fri=None, open_sat=None, close_sat=None, open_sun=None, close_sun=None):
    sql = text(f"""INSERT INTO restaurants (name, description, address, coord_x, coord_y, 
                is_24h, open_mon, close_mon, open_tue, close_tue, open_wed, close_wed, open_thu, close_thu,
                open_fri, close_fri, open_sat, close_sat, open_sun, close_sun)
                VALUES (:name, :description, :address, :coord_x, :coord_y, 
                :is_24h, :open_mon, :close_mon, :open_tue, :close_tue, :open_wed, :close_wed, :open_thu, :close_thu,
                :open_fri, :close_fri, :open_sat, :close_sat, :open_sun, :close_sun)""")
    db.session.execute(sql, {"name":name, "description":description, "address":address, "coord_x":coord_x, "coord_y":coord_y,
                             "is_24h":is_24h, "open_mon":open_mon, "close_mon":close_mon, "open_tue":open_tue, "close_tue":close_tue,
                             "open_wed":open_wed, "close_wed":close_wed, "open_thu":open_thu, "close_thu":close_thu, "open_fri":open_fri,
                             "close_fri":close_fri, "open_sat":open_sat, "close_sat":close_sat, "open_sun":open_sun, "close_sun":close_sun,})
    db.session.commit()
    return True

def comment(comment, rating, restaurant_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    restaurant_id = get_details(restaurant_name).id
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

def edit_restaurant(res_id, name, description, address, coord_x, coord_y, is_24h,
            open_mon=None, close_mon=None, open_tue=None, close_tue=None, open_wed=None, close_wed=None, open_thu=None, close_thu=None,
           open_fri=None, close_fri=None, open_sat=None, close_sat=None, open_sun=None, close_sun=None):
    sql = text(f"""UPDATE restaurants SET name=:name, description=:description, address=:address, coord_x=:coord_x, coord_y=:coord_y, 
                is_24h=:is_24h, open_mon=:open_mon, close_mon=:close_mon, open_tue=:open_tue, close_tue=:close_tue, open_wed=:open_wed, close_wed=:close_wed,
               open_thu=:open_thu, close_thu=:close_thu, open_fri=:open_fri, close_fri=:close_fri, open_sat=:open_sat, close_sat=:close_sat, open_sun=:open_sun, close_sun=:close_sun
               WHERE id={res_id}""")
    db.session.execute(sql, {"name":name, "description":description, "address":address, "coord_x":coord_x, "coord_y":coord_y,
                             "is_24h":is_24h, "open_mon":open_mon, "close_mon":close_mon, "open_tue":open_tue, "close_tue":close_tue,
                             "open_wed":open_wed, "close_wed":close_wed, "open_thu":open_thu, "close_thu":close_thu, "open_fri":open_fri,
                             "close_fri":close_fri, "open_sat":open_sat, "close_sat":close_sat, "open_sun":open_sun, "close_sun":close_sun,})
    db.session.commit()
    return True

def get_today_weekday():
    today = datetime.datetime.today()
    weekday_name = today.strftime('%a').lower()
    return weekday_name
