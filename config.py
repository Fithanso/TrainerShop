import datetime
import os


class Configuration:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/ShopDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # permanent_session_lifetime = datetime.timedelta(days=10)
#     "mysql+pymysql://root:password@localhost:3306/public"
