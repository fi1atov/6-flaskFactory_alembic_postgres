class Config:
    SECRET_KEY = 'dev'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/skillbox_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class AutoTestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/skillbox_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False



config = {
    'development': DevelopmentConfig,
    'autotesting': AutoTestConfig,
}
