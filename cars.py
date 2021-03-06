from db import db

def get_car_id_by_ad_id(id):
    sql = "SELECT car_id FROM ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()
    db.session.commit()
    return result[0]

def get_all_car_info_by_id(id):
    sql = "SELECT * FROM cars WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    car_data = result.fetchall()
    db.session.commit()
    return car_data

def add_car_and_return_id(brand, model, chassis, fuel, drive, transmission, mileage, year, price, color, engine, power, legal):
    sql = "INSERT INTO cars (brand, model, chassis, fuel, drive, transmission, mileage, year, price, " \
          "color, engine, power, street_legal) VALUES " \
          "(:brand, :model, :chassis, :fuel, :drive, :transmission, :mileage, :year, :price, :color, " \
          ":engine, :power, :street_legal) RETURNING id"
    result = db.session.execute(sql, {"brand":brand, "model":model, "chassis":chassis,
                                      "fuel":fuel, "drive":drive, "transmission":transmission,
                                      "mileage":mileage, "year":year, "price":price, "color":color,
                                      "engine":engine, "power":power, "street_legal":legal})
    car_id = result.fetchone()[0]
    return car_id

def update_car_data(brand, model, chassis, fuel, drive, transmission, mileage, year, price, color, engine, power, legal, id):
    sql = "UPDATE cars SET brand=:brand, model=:model, chassis=:chassis, fuel=:fuel, drive=:drive, " \
          "transmission=:transmission, mileage=:mileage, year=:year, price=:price, color=:color, " \
          "engine=:engine, power=:power, street_legal=:legal WHERE id=:id"
    db.session.execute(sql, {"brand":brand, "model":model, "chassis":chassis, "fuel":fuel, "drive":drive,
                             "transmission":transmission, "mileage":mileage, "year":year, "price":price,
                             "color":color, "engine":engine, "power":power, "legal":legal, "id":id})