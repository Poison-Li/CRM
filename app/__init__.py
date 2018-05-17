from flask import Flask
from config import Config
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
#
# mysql = MySQL()
# mysql.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'you never guess'

from app.customer import bp as customer_bp
app.register_blueprint(customer_bp, url_prefix='/customer')

from app.product import bp as product_bp
app.register_blueprint(product_bp, url_prefix='/product')

from app.trade import bp as trade_bp
app.register_blueprint(trade_bp, url_prefix='/trade')
