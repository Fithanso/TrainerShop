from flask import *
from flask_sqlalchemy import *
from flask_migrate import *
from config import Configuration


application = Flask(__name__)

application.config.from_object(Configuration)
application.secret_key = os.urandom(24)
db = SQLAlchemy(application, session_options={"autoflush": False})
migrate = Migrate(application, db)







