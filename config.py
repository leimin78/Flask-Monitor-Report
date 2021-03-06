# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'report and monitor'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(self):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DATABASE_URI = os.path.join(basedir, 'data.sqlite')


class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = """mysql://root:123456@localhost/csmonitor"""


config = {
'development': DevelopmentConfig,
'testdb':TestConfig
}


print(basedir)
