from marshmallow_sqlalchemy import ModelSchema
from app.cars.models import Car, CarData
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cars = db.relationship('Car', backref='author', lazy=True)

    
class UserSchema(ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

