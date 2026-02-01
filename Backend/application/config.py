class BaseConfig():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECRET_KEY = "gvkbhdbfmnvnvbekgonopfwhfhkbf"

    # Flask-Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/2" 
    CACHE_DEFAULT_TIMEOUT = 60
