from flask import *
from flask_sqlalchemy import *
from flask_migrate import *
from config import Configuration


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

SMALLINT_MAX = 32767
SMALLINT_LEN = 5
INT_MAX = 2147483647
INT_LEN = 10
BIGINT_MAX = 9223372036854775807
BIGINT_LEN = 19





