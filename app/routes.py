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

@app.route('/')
@app.route('/index')
def welcome():
    latest_question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).first()
    return render_template('welcome_page.html', latest_question = latest_question)

@app.route('/forum_page')
def forum_page():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forums.html', questions=questions)

@app.route('/question/<int:question_id>')
def question_details(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    return render_template('question_details.html', question=question)