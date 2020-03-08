from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['PER_PAGE'] = 6
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mhtsdvfq:yOhNRqRkv7XmSoYEMY4pgvM3AmrpTC-0@kandula.db.elephantsql.com:5432/mhtsdvfq'
migrate = Migrate(app, db)
api = Api(app, version='1.0', title='SYC API')

from app.users.controllers import users
from app.cars.controllers import cars
from app.reminders.controllers import reminders
api.add_namespace(users)
api.add_namespace(cars)
api.add_namespace(reminders)

db.create_all()


