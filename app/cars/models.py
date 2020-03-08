from datetime import datetime, timedelta
from app import db
from marshmallow_sqlalchemy import ModelSchema

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)
    matriculation = db.Column(db.DateTime, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    carData = db.relationship('CarData', backref='car_author', lazy=True)

    def __repr__(self):
        return f"Car('{self.name}', '{self.matriculation}', '{self.fuel}','{self.image_file}', {self.carData}')"

class CarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataInt = db.Column(db.Integer, nullable=True, default=0)
    dataDate = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    carDataCode = db.Column(db.Integer, nullable=False)
    id_car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    id_reminder = db.Column(db.Integer, db.ForeignKey('reminder.id'), nullable=True)
    
    def __repr__(self):
        return f"CarData('{self.dataInt}', '{self.dataDate}')"

    # Metodo che occorre ad aggiungere dati di tipo intero nella tabella CarData
    @staticmethod
    def add_dataInt(car,carDataCode,value):
        carValue = CarData(dataInt = value, carDataCode = carDataCode, car_author = car )
        db.session.add(carValue)

    # Metodo che occorre ad aggiungere dati di tipo DateTime nella tabella CarData
    @staticmethod
    def add_dataDate(car,carDataCode,value):
        carValue = CarData(dataDate = datetime.strptime(value, '%m/%d/%Y'), carDataCode = carDataCode, car_author = car )
        db.session.add(carValue)

    # Metodo che occorre ad aggiornare dati di tipo intero nella tabella CarData
    @staticmethod
    def update_dataInt(car,carDataCode,value):
        car_data =CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=carDataCode).first()
        car_data.dataInt = value
    
    # Metodo che occorre ad aggiornare dati di tipo DateTime nella tabella CarData
    @staticmethod
    def update_dataDate(car,carDataCode,value):
        car_data =CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=carDataCode).first()
        car_data.dataDate = datetime.strptime(value, '%m/%d/%Y')

    # Metodo che ritorna i km medi associati ad un'auto
    @staticmethod
    def GetKm(car, carvalues):
	    for carvalue in carvalues:
		    if carvalue.carDataCode == 6:
			    kmMedi = carvalue.dataInt
			    return kmMedi

    # Metodo che ritorna il chilometraggio inserito dall'utente 
    # e la data del suo rilevamento
    @staticmethod
    def GetDateDetection(car, carvalues):
	    for carvalue in carvalues:
		    if carvalue.carDataCode == 1:
			    rilievo = [carvalue.dataDate, carvalue.dataInt]
			    return rilievo

    # Metodo che ritorna True in caso l'auto abbia bisogno della revisione
    # False in caso contrario.
    @staticmethod
    def revisione(car, value):
        if ((((datetime.now() - value >= timedelta(days=730) - timedelta(days=30)) 
				and 
				(datetime.now() - car.matriculation >= timedelta(days=1460)) 
				)
				or 
				(
				(datetime.now() - car.matriculation < timedelta(days=1460))
				and (timedelta(days=1460) - (datetime.now() - car.matriculation) <= timedelta(days=30)) 
				)
				)):
                return True
        else:
		        return False
    
    # Metodo che ritorna True in caso l'auto abbia bisogno di essere assicurata,
    # False in caso contrario.
    @staticmethod
    def assicurazione(car, date):
        if (datetime.now() >= date - timedelta(days=30)):
            return True 
        else:
            return False

    # Metodo che ritorna True in caso l'auto abbia bisogno di un tagliando,
    # False in caso contrario.
    @staticmethod
    def tagliando(car, value, kmMedi, rilievo):
        if (
			((rilievo[1] + (kmMedi*((datetime.now() - rilievo[0])/timedelta(days=7))))-value > 30000)
			):
            return True 
        else:
            return False

    # Metodo che ritorna True in caso il bollo stia per scadere,
    # False in caso contrario.
    @staticmethod
    def bollo(car, value):
        if (datetime.now() >= value - timedelta(days=30)):
            return True
        else:
            return False

    # Metodo che ritorna True in caso l'auto necessiti della revisione,
    # False in caso contrario.
    @staticmethod
    def revisione(car, value):
        if ((((datetime.now() - value >= timedelta(days=730) - timedelta(days=30)) 
				and 
				(datetime.now() - car.matriculation >= timedelta(days=1460)) 
				)
				or 
				(
				(datetime.now() - car.matriculation < timedelta(days=1460))
				and 
				(timedelta(days=1460) - (datetime.now() - car.matriculation) <= timedelta(days=30)) 
				)
				)):
                return True
        else:
            return False
	    



class CarSchema(ModelSchema):
    class Meta:
        model = Car
        sqla_session = db.session

class CarDataSchema(ModelSchema):
    class Meta:
        model = CarData
        sqla_session = db.session
