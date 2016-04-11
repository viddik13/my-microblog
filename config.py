import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# mail server settings
MAIL_SERVER   = '127.0.0.1'
MAIL_PORT     = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# admin list
ADMINS = ['viddik13@gmail.com']