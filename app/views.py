from flask import render_template, flash, redirect, session
from flask import url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from .forms import LoginForm, ProfileEditForm
from .models import User
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'Feofan'},
            'body': 'It\'s cold in the forest!!'
        },
        {
            'author': {'nickname': 'Feofan'},
            'body': "Better dance some D'n'B!!"
        }
    ]

    return render_template("index.html", title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    l_form = LoginForm()

    if l_form.validate_on_submit():
        session['remember_me'] = l_form.remember_me.data
        nickname, email = l_form.username.data, l_form.email.data

        user = User.query.filter_by(email=email).first()

        if user is None:

            if nickname is None or nickname == "":
                nickname = email.split('@')[0]

            user = User(nickname=nickname, email=email)
            print "***Database operation: adding user..."
            db.session.add(user)
            db.session.commit()

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)

        login_user(user, remember_me)

        return redirect(request.args.get('next') or url_for('index'))

    return render_template("login.html",
                           title="Sign In",
                           form=l_form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %r not found.' % nickname)
        return redirect(url_for('index'))

    posts = [
        {'author': user, 'body': "This is madness!"},
        {'author': user, 'body': "THIS IS SPARTAAA!!!"}
    ]

    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = ProfileEditForm()
    if edit_form.validate_on_submit():
        g.user.nickname = edit_form.nickname.data
        g.user.about_me = edit_form.about_me.data
