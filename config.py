import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'CRM.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
