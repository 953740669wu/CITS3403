import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # set the email system
    MAIL_DEBUG = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    
    MAIL_USERNAME = "wu953740669@gmail.com"
    MAIL_PASSWORD = "efzd zwkd twvc snnf"
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    ADMINS = ["wu953740669@gmail.com"]  # Add ADMINS here

    
   

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False