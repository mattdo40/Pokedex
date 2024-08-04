class BaseConfig:
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///pokemon.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = 'pokemon.db'

class ProductionConfig(BaseConfig):
    DATABASE_URI = 'pokemon.db'