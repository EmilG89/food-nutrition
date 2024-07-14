from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.widgets import Input
from models import Food


with app.app_context():

    item = Food.query.first()
    elements = item.elements.all()
    elements_names = []
    for element in elements:
        elements_names.append(element.name)
    
    elements_names[0] = 'Elements'
    
    x = Food.query.with_entities(Food.name).all()
    food_names = []
    for name in x:
        food_names.append(name[0])
    
    food_names[0] = "Food Items"

    class RegistrationForm(FlaskForm):
        username = StringField("Username", validators=[DataRequired()])
        email = StringField("Email", validators=[DataRequired(), Email()])
        password = PasswordField("Password", validators=[DataRequired()])
        password_r = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
        #add BoolField sign up for healthy meal recipes, diet recomendations and fun facts
        submit = SubmitField("Register")

    class LoginForm(FlaskForm):
        email = StringField("Email", validators=[DataRequired(), Email()])
        password = PasswordField("Password", validators=[DataRequired()])
        remember = BooleanField("Remember Me")
        submit = SubmitField("Log In")

    class ElementForm(FlaskForm):
        element = SelectField("Element", choices=elements_names)
        submit = SubmitField("Find")
    
    class FoodForm(FlaskForm):
        item = SelectField("Food", choices=food_names)
        submit = SubmitField("Find")
