from app import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.Integer, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def avatar(self, size):
        return ''

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        
class OUser(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique = True)
    email = db.Column(db.String(80), unique = True)
    
    def __repr__(self)
        return '<OUser %r>' % (self.email)