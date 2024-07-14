from flask import Flask, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DecimalField, FloatField, FileField, FormField, HiddenField, IntegerField, MultipleFileField, PasswordField, RadioField, SelectField, SelectMultipleField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'security_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_app.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

tables = []
tables1 = []

@app.route("/", methods=["GET", "POST"])
def index():
    element_form = forms.ElementForm()
    food_form = forms.FoodForm()

    if element_form.validate_on_submit():
        tables.clear()
        element_items = models.Element.query.filter(db.and_(models.Element.name == element_form.element.data, \
                                                    models.Element.value > 0, models.Element.value != "", \
                                                    models.Element.food_name != 'English name')).\
                                                    order_by(models.Element.value.desc()).limit(100).all()
        table = []
        for n, item in enumerate(element_items):
            table.append((n+1, item))
            if len(table) == 20:
                tables.append(table)
                table = []
            elif n+1 == len(element_items):
                tables.append(table)
                table = []
        
        return render_template("home.html", element_form=element_form, food_form=food_form, tables=tables, tables1=tables1)
    
    item = None
    if request.args.get("name"):
        item = item_details(request.args.get("name"))

    if item:
        elements = item.elements
        elements = sorted(elements, reverse=True, key=lambda e: [e.value if isinstance(e.value, int) or \
                                                                 isinstance(e.value, float) else 0])
        elements.append(item.name)
        return render_template("home.html", element_form=element_form, food_form=food_form, tables=tables, tables1=tables1, elements = elements)

    if food_form.validate_on_submit():
        tables1.clear()
        elements = models.Element.query.filter(db.and_(models.Element.food_name == food_form.item.data, \
                                                models.Element.value > 0, models.Element.value != "", \
                                                models.Element.name != 'name')).\
                                                order_by(models.Element.value.desc()).all()

        table1 = []
        for n, item in enumerate(elements):
            table1.append((n+1, item))
            if len(table1) == 20:
                tables1.append(table1)
                table1 = []
            elif n+1 == len(elements):
                tables1.append(table1)
                table1 = []
    
        return render_template("home.html", element_form=element_form, food_form=food_form, tables=tables, tables1=tables1)

    return render_template("home.html", element_form=element_form, food_form=food_form,)

@app.route("/food_data", methods=["GET", "POST"])
def food_data_page():
    all_food = models.Food.query.all()
    elements = all_food[0].elements.all()
    return render_template("food_data.html", all_food = all_food, elements = elements)

@app.route("/human_physiology")
@login_required
def human_physiology_page():
    return render_template("human_physiology.html")

@app.route("/relevant_articles")
def relevant_articles_page():
    return render_template("relevant_articles.html")

@app.route("/build_a_diet")
def build_a_diet_page():
    return render_template("build_a_diet.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():

    reg_form = forms.RegistrationForm()
    if reg_form.validate_on_submit():
        reg_user = models.User(username = reg_form.username.data, email = reg_form.email.data)
        reg_user.set_password(reg_form.password.data)
        db.session.add(reg_user)
        db.session.commit()
        flash("Thank you for registration!")
    
    log_form = forms.LoginForm() 
    if log_form.validate_on_submit():
       log_user = models.User.query.filter_by(email=log_form.email.data).first()
       if log_user and log_user.check_password(log_form.password.data):
           login_user(log_user)
           next_page = request.args.get("next")
           return redirect(next_page) if next_page else redirect(url_for("index", _external=True, _scheme="http"))
       else:
           flash("Invalid email or password!")
    
    return render_template("login.html", reg_form = reg_form, log_form = log_form)

def item_details(item):
    item = models.Food.query.filter_by(name = item).first()
    return item

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_page"))

import models
import forms
