from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class ProfileEditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])