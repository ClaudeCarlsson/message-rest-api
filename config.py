import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'messages.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False