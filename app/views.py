from flask import render_template, flash, redirect, session
from flask import url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    print ">>> index"
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'Feofan' },
            'body': 'It\'s cold in the forest!!'
        },
        {
            'author': { 'nickname': 'Feofan' },
            'body': "Better dance some D'n'B!!"
        }
    ]

    return render_template("index.html",
                           title = 'Home',
                           user = user,
                           posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
#@oid.loginhandler
def login():
    print ">>> login"
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    l_form = LoginForm()
    
    if l_form.validate_on_submit():
        session['remember_me'] = l_form.remember_me.data
        nickname = l_form.username.data
        email = l_form.email.data

        user = User.query.filter_by(email=email).first()

        if user is None:

            if nickname is None or nickname == "":
                nickname = email.splint('@')[0]

            new_user = User(nickname=nickname, email=email)
            print "***Database operation: adding user..."
            db.session.add(new_user)
            db.session.commit()
            user = new_user

        login_user(user)

        return redirect(request.args.get('next') or url_for('index'))
        #return oid.try_login(l_form.openid.data, ask_for=['nickname', 'email'])

    return render_template("login.html",
                           title = "Sign In",
                           form = l_form,
                           providers = app.config['OPENID_PROVIDERS'])

@app.before_request
def before_request():
    g.user = current_user
    print g.user

#@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        print "***after_login: no email"
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.splint('@')[0]
        user = User(nickname=nickname, email=resp.email)
        print "***Database operation: adding user..."
        db.session.add(user)
        db.session.commit()
    
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
        
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User % not found.' % nickname)
        return redirect(url_for('index'))

    posts = [
        {'author': user, 'body': "This is madness!"},
        {'author': user, 'body': "THIS IS SPARTAAA!!!"}
    ]

    return render_template('user.html',
                           user=user,
                           posts=posts)