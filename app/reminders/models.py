from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from app import db
from app.cars.models import CarData

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    carsdata = db.relationship('CarData', backref='reminder', lazy=True)

    def __repr__(self):
        return f"Reminder('{self.text}')"

class ReminderSchema(ModelSchema):
    class Meta:
        model = Reminder
        sqla_session = db.session
