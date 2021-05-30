import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER =""
    MAIL_PORT = 587
    MAIL_USE_TLS =True
    MAIL_USE_SSL = False
    MAIL_DEBUG =True
    MAIL_USERNAME =""
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = ""
    MAIL_MAX_EMAILS =None
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS =False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True