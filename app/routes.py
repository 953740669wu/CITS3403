from flask import render_template, request, redirect, url_for, flash, get_flashed_messages,session,jsonify
from app import app, db
from app.forms import LoginForm, StaffLoginForm
from app.models import UserModel, QuestionModel, AnswerModel, EventModel,LikeModel,CommentModel
from flask_mail import Message
from flask_login import logout_user, login_required, current_user, login_user
from app.forms import RegistrationForm, QuestionForm, AnswerForm, EventForm
from sqlalchemy import select
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def welcome():
    latest_question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).first()
    return render_template('welcome_page.html', latest_question=latest_question)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    customer_login_form = LoginForm()
    staff_login_form = StaffLoginForm()
    
    if request.method == 'POST':
        if customer_login_form.validate_on_submit():
            username = customer_login_form.username.data
            password = customer_login_form.password.data
            
            user = UserModel.query.filter_by(username=username).first()
            if user is None:
                flash('User not registered.', 'error')
                return redirect(url_for('login'))
            if not user.check_password(password):
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))
            
            # Logic for successful customer login
            login_user(user)
            session['message'] = 'Customer login successful!'
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return jsonify({'redirect': next_page, 'message': session.pop('message')})
        
        elif staff_login_form.validate_on_submit():
            staff_username = staff_login_form.staff_username.data
            staff_password = staff_login_form.staff_password.data

            staff = UserModel.query.filter_by(username=staff_username).first()
            if staff is None:
                flash('Staff user not registered.', 'error')
                return redirect(url_for('login'))
            if not staff.check_password(staff_password):
                flash('Invalid staff username or password.', 'error')
                return redirect(url_for('login'))
            
            # Logic for successful staff login
            login_user(staff)
            session['message'] = 'Staff login successful!'
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return jsonify({'redirect': next_page, 'message': session.pop('message')})

    return render_template('login.html', form=customer_login_form, staff_form=staff_login_form)
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Register', form=form)

#Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/event', methods=['GET'])
def event_page():
    events = EventModel.query.all()
    return render_template('event_page.html', events = events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = EventModel.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/forum_page')
def forum_page():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forums.html', questions=questions)

@app.route('/question/<int:question_id>')
def question_details(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    return render_template('question_details.html', question=question)

@app.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("forums.html", questions=questions)

@app.route("/public_question", methods=['GET', 'POST'])
@login_required
def forum_p_page():
    form = QuestionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=current_user)
            db.session.add(question)
            db.session.commit()
            flash('问题成功发布！')
            return redirect('/')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f"错误在 {fieldName}: {err}")
    return render_template('public_question.html', form=form)

@app.route("/answer/public", methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=current_user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("question_details", question_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("question_details", question_id=request.form.get("question_id")))


@app.route('/toys_page')
def toys_page():
    return 'This is the toys page.'

@app.route('/food_page')
def food_page():
    return 'This is the food page.'

@app.route('/health_page')
def health_page():
    return 'This is the health page.'

@app.route('/hotel_page')
def hotel_page():
    return 'This is the hotel page.'


@app.route('/user/<username>')
@login_required
def user(username):
    user = UserModel.query.filter_by(username=username).first_or_404()
    questions = QuestionModel.query.filter_by(author_id=user.id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('my_questions.html', user=user, questions=questions)


@app.route('/my_questions', methods=['GET'])
@login_required
def my_questions():
    questions = QuestionModel.query.filter_by(author_id=current_user.id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('my_questions.html', questions=questions)

@app.route('/question/delete/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    question = QuestionModel.query.get_or_404(question_id)
    if question.author_id != current_user.id:
        flash('You do not have permission to delete this question.', 'error')
        return redirect(url_for('forum_page'))
    
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully.')
    return redirect(url_for('forum_page'))
