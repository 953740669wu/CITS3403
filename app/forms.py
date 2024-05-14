import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from app.models import UserModel