from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, StaffLoginForm
from app.models import UserModel, QuestionModel, AnswerModel
from flask_mail import Message
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from app.forms import RegistrationForm, QuestionForm, AnswerForm
from sqlalchemy import select