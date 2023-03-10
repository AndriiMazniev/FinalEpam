class Config:
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:sqlpass@192.168.99.100:3306/db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


