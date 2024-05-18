from flask import render_template, request, redirect, url_for, flash, get_flashed_messages, session, jsonify
from app.extensions import db
from app.forms import LoginForm, StaffLoginForm
from app.models import UserModel, QuestionModel, AnswerModel, EventModel, LikeModel, CommentModel
from flask_mail import Message
from flask_login import logout_user, login_required, current_user, login_user
from app.forms import RegistrationForm, QuestionForm, AnswerForm, EventForm
from sqlalchemy import select
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
from .blueprints import main
import os

@main.route('/')
@main.route('/index')
def welcome():
    latest_question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).first()
    latest_event = EventModel.query.order_by(EventModel.create_time.desc()).first()
    return render_template('welcome_page.html', latest_question=latest_question, latest_event=latest_event)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page', posts=posts)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    customer_login_form = LoginForm()

    if request.method == 'POST':
        if customer_login_form.validate_on_submit():
            username = customer_login_form.username.data
            password = customer_login_form.password.data
            
            user = UserModel.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password.', 'error')
                return redirect(url_for('main.login'))
            
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)

    return render_template('login.html', form=customer_login_form)

@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('sign_up.html', title='Register', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@main.route('/event', methods=['GET'])
def event_page():
    events = EventModel.query.all()
    return render_template('event_page.html', events=events)

@main.route('/event/<int:event_id>')
def event_details(event_id):
    event = db.session.get(EventModel, event_id)
    comments = CommentModel.query.filter_by(event_id=event_id).all() 
    return render_template('event_detail.html', event=event, comments=comments)

@main.route('/forum_page')
def forum_page():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forums.html', questions=questions)

@main.route('/question/<int:question_id>')
def question_details(question_id):
    question = db.session.get(QuestionModel, question_id)
    return render_template('question_details.html', question=question)

@main.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("forums.html", questions=questions)

@main.route("/public_question", methods=['GET', 'POST'])
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
            
            return redirect('/')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f"错误在 {fieldName}: {err}")
    return render_template('public_question.html', form=form)

@main.route("/answer/public", methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=current_user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("main.question_details", question_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("main.question_details", question_id=request.form.get("question_id")))

@main.route('/user/<username>')
@login_required
def user(username):
    user = UserModel.query.filter_by(username=username).first_or_404()
    questions = QuestionModel.query.filter_by(author_id=user.id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('my_questions.html', user=user, questions=questions)

@main.route('/my_questions', methods=['GET'])
@login_required
def my_questions():
    questions = QuestionModel.query.filter_by(author_id=current_user.id).order_by(QuestionModel.create_time.desc()).all()
    return render_template('my_questions.html', questions=questions)

@main.route('/question/delete/<int:question_id>', methods=['POST'])
@login_required
def delete_question(question_id):
    question = db.session.get(QuestionModel, question_id)
    if question.author_id != current_user.id:
        flash('You do not have permission to delete this question.', 'error')
        return redirect(url_for('main.forum_page'))
    
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully.')
    return redirect(url_for('main.forum_page'))

@main.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = EventModel(
            title=form.title.data,
            location=form.location.data,
            description=form.description.data,
            author_id=current_user.id,
            event_time=form.event_time.data
        )
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    return render_template('create_event.html', form=form)

@main.route('/like_event/<int:event_id>', methods=['POST'])
@login_required
def like_event(event_id):
    existing_like = LikeModel.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if existing_like:
        return jsonify({'status': 'error', 'message': 'You have already liked this event.'}), 200

    event = db.session.get(EventModel, event_id)
    if event.author_id == current_user.id:
        return jsonify({'status': 'error', 'message': 'You cannot like your own event.'}), 200

    like = LikeModel(event_id=event_id, user_id=current_user.id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Event liked successfully.'})

@main.route('/comment', methods=['POST'])
@login_required
def comment_event():
    data = request.json
    event_id = data.get('event_id')
    content = data.get('content')

    if not event_id or not content:
        return jsonify({'error': 'Missing event_id or content'}), 200

    existing_comment = CommentModel.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if existing_comment:
        return jsonify({'status': 'error', 'message': 'You have already commented on this event.'}), 200

    event = db.session.get(EventModel, event_id)
    if event.author_id == current_user.id:
        return jsonify({'status': 'error', 'message': 'You cannot comment on your own event.'}), 200

    comment = CommentModel(event_id=event_id, user_id=current_user.id, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully'}), 200
