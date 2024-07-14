from app import app, db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():

    class Food(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String(50), index = True, unique = True)
        #add description about food
        elements = db.relationship("Element", backref = "food", lazy = "dynamic")
#        diet = db.relationship("Diet", backref = "food", lazy = "dynamic")
    
    class Element(db.Model):
        header_id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String, index = True)
        value = db.Column(db.Integer, index = True)
        #add description about eleent
        food_name = db.Column(db.String, db.ForeignKey("food.name"))
    
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(50), index = True, unique = True)
        password_hash = db.Column(db.String(128))
        email = db.Column(db.String(50))
        joined_at = db.Column(db.DateTime(), default = datetime.now(), index = True)
 #       diet = db.relationship("Diet", backref = "user", lazy="dynamic")

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

#    class Diet(db.Model):
#        id = db.Column(db.Integer, primary_key = True)
#        user = db.Column(db.String, db.ForeignKey("user.username"))
#        food = db.Column(db.String, db.ForeignKey("food.name"))
