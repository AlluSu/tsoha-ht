from flask.templating import render_template
from db import db
import users

def remove_ad(ad_id, user_id):
    sql = "UPDATE ads SET visible=False WHERE user_id=:logged AND ads.id=:id"
    db.session.execute(sql, {"logged":user_id, "id":ad_id})
    db.session.commit()

def remove_ad_as_admin(ad_id):
    sql = "UPDATE ads SET visible=False WHERE ads.id=:id"
    db.session.execute(sql, {"id":ad_id})
    db.session.commit()

def add_image(name, data, ad_id):
    sql = "INSERT INTO images (name,data) VALUES (:name,:data) RETURNING id"
    result = db.session.execute(sql, {"name":name, "data":data})
    image_id = result.fetchone()[0]

    sql = "INSERT INTO ad_images (image_id,ad_id) VALUES (:image_id,:ad_id)"
    db.session.execute(sql, {"image_id":image_id, "ad_id":ad_id})
    db.session.commit()

def add_ad_and_return_id(info, car_id):
    sql = "INSERT INTO ads (info, created, visible, user_id, car_id) VALUES " \
          "(:info, NOW(), :visible, :user_id, :car_id) RETURNING id"
    result = db.session.execute(sql, {"info":info, "visible":True, "user_id":users.get_user_id(), "car_id":car_id})
    ad_id = result.fetchone()[0]
    db.session.commit()
    return ad_id

def create_reference(car_id, ad_id):
    sql = "INSERT INTO car_ad (car_id, ad_id) VALUES (:car_id, :ad_id)"
    db.session.execute(sql, {"car_id":car_id, "ad_id":ad_id})

def ads_by_user_id(id, status):
    sql = "SELECT c.brand, c.model, c.mileage, c.year, c.price, a.id, a.info, a.created FROM cars c, ads a WHERE " \
        "a.user_id=:id AND c.id=a.car_id AND a.visible=:visible"
    result = db.session.execute(sql, {"id":id, "visible":status})
    ads = result.fetchall()
    return ads

def get_essential_car_data():
    sql = "SELECT c.id, c.brand, c.model, c.mileage, c.year, c.price FROM " \
          "cars c, ads a WHERE c.id=a.car_id " \
          "AND a.visible=True ORDER BY a.created DESC"
    result = db.session.execute(sql)
    cars = result.fetchall()
    db.session.commit()
    return cars