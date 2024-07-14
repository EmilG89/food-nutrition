from app import app, db
from models import Food, Element
import csv

with open("foodData/food_database_short.csv") as food_data:
    data_list = csv.DictReader(food_data, delimiter=";")

    with app.app_context():

        for data in data_list:
            print(data)
            item = Food(name = data["name"])
            db.session.add(item)
            db.session.commit()
            print(data["name"])

            item_data = {}
            for key, value in data.items():
                item_data["name"] = key #add strip
                item_data["value"] = value
                item_data["food_name"] = item.name
                element = Element(**item_data)
                db.session.add(element)
                db.session.commit()
                print(item_data)

        db.session.close()

