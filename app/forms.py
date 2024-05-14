import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from app.models import UserModel

class LoginForm(FlaskForm):
    pass

class StaffLoginForm(FlaskForm):
    pass

class RegistrationForm(FlaskForm):
    pass

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class AnswerForm(wtforms.Form):
    pass