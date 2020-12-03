from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email

class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    email = StringField("Email:", validators=[InputRequired(), Email()])
    first_name = StringField("First Name:", validators=[InputRequired()])
    last_name = StringField("Last Name:", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("title:", validators=[InputRequired()])
    content = TextAreaField("content:", validators=[InputRequired()])


