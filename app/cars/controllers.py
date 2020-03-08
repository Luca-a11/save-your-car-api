from flask import jsonify, request
from flask_restplus import Resource, reqparse, fields
from app.cars.models import Car, CarData, CarSchema, CarDataSchema
from app import api
from app import db
from app import app
from datetime import datetime

cars = api.namespace('api/v1.0/cars',description='CRUD operation for syc cars')

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
car_data_schema = CarDataSchema()

carModel = cars.model('carModel', {
    'name' : fields.String(required=True, validate=True),
    'fuel' : fields.String(required=True, validate=True),
    'matriculation': fields.DateTime(validate=True),
    'image_file' : fields.String(validate=True),
    'detected_kms': fields.Integer(validate=True),
    'review_date': fields.DateTime(validate=True),
    'check_km': fields.Integer(validate=True),
    'assurance_date': fields.DateTime(validate=True),
    'tax_date': fields.DateTime(validate=True),
    'avarage_km': fields.Integer(validate=True)
})

parserId = reqparse.RequestParser()
parserId.add_argument('car_id',type=int)

parserUserId = reqparse.RequestParser()
parserUserId.add_argument('id_user',type=int)

parserPage = reqparse.RequestParser()
parserPage.add_argument('page',type=int, default=1)


@cars.route('/<int:car_id>')
class CarById_Requests(Resource):
    def get(self,car_id):
        '''get a car'''
        car = Car.query.get(car_id)
        if not car:
            return 'car Not Found', 404
        response={}
        response['car']= car_schema.dump(car)
        response['car_data'] = []
        for car_data in car.carData:
            response['car_data'].append(car_data_schema.dump(car_data))
        return jsonify(response)

    @cars.expect(carModel,parserUserId , validate=True)
    def put(self,car_id):
        '''update car data'''
        car = Car.query.get(car_id)
        if not car:
           return 'car Not Found', 404
        car.name = request.get_json()['name'] if request.get_json()['name'] else car.name
        car.fuel = request.get_json()['fuel'] if request.get_json()['fuel'] else car.fuel
        car.image_file =  request.get_json()['image_file'] if request.get_json()['image_file'] else car.image_file
        car.matriculation =  datetime.strptime(request.get_json()['matriculation'], '%m/%d/%Y') if request.get_json()['matriculation'] else car.matriculation
        car.id_user = request.args.get('id_user') if request.args.get('id_user') else car.id_user
        db.session.commit()
        car_data = request.get_json()
        detected_kms = CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=1).first()
        print(detected_kms)
        detected_kms = car_data.get('detected_kms') if car_data.get('detected_kms') else CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=1).first().dataInt
        CarData.update_dataInt(car,1,detected_kms) 
        if request.get_json()['review_date']:
            CarData.update_dataDate(car,2,request.get_json()['review_date'])
        check_km= request.get_json()['check_km'] if request.get_json()['check_km'] else CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=3).first().dataInt
        CarData.update_dataInt(car,3,check_km)
        if request.get_json()['assurance_date']:
            CarData.update_dataDate(car,4,request.get_json()['assurance_date'])
        if request.get_json()['tax_date']:
            CarData.update_dataDate(car,5,request.get_json()['tax_date'])
        avarage_km= request.get_json()['avarage_km'] if request.get_json()['avarage_km'] else CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=6).first().dataInt
        CarData.update_dataInt(car,6,avarage_km)
        db.session.commit()
        return jsonify(car_schema.dump(car))

    @cars.expect(parserUserId)
    def delete(self,car_id):
        '''delete a car'''
        try:
            id_user = int(request.args.get('id_user'))
            car = Car.query.get(car_id)
            if not car:
                return 'Car Not Found', 404
            elif id_user == car.id_user:
                for car_data in car.carData:
                    db.session.delete(car_data)
                db.session.commit()
                db.session.delete(car)
                db.session.commit()
                return jsonify({'result': True})
            else:
                return 'Action Forbidden', 403
        except:
            return 'Error Server Side', 500

@cars.route('/<int:car_id>/<int:car_data_code>')
class GET_DataByCode(Resource):
    def get(self,car_id,car_data_code):
        '''get a car_data by code'''
        car = Car.query.get(car_id)
        if not car:
            return 'car Not Found', 404
        car_data=CarData.query.filter_by(id_car=car.id).filter_by(carDataCode=car_data_code).first()
        if not car_data:
            return 'car_data Not Found', 404
        return jsonify(car_data_schema.dump(car_data))


@cars.route('')
class General_Car_Requests(Resource):
    @cars.expect(carModel,parserUserId, validate=True)
    def post(self):
            '''register a car'''
            name = request.get_json()['name'] 
            fuel = request.get_json()['fuel']
            image_file =  request.get_json()['image_file'] 
            matriculation =  request.get_json()['matriculation']
            id_user=request.args.get('id_user')
            new_car = Car(
            name=name,
            matriculation=datetime.strptime(matriculation, '%m/%d/%Y'),
            image_file=image_file,
            fuel=fuel,
            id_user=id_user)
            db.session.add(new_car)
            db.session.commit()
            detected_kms= request.get_json()['detected_kms']
            CarData.add_dataInt(new_car,1,detected_kms)
            review_date= request.get_json()['review_date']
            CarData.add_dataDate(new_car,2,review_date)
            check_km= request.get_json()['check_km']
            CarData.add_dataInt(new_car,3,check_km)
            assurance_date= request.get_json()['assurance_date']
            CarData.add_dataDate(new_car,4,assurance_date)
            tax_date= request.get_json()['tax_date']
            CarData.add_dataDate(new_car,5,tax_date)
            avarage_km= request.get_json()['avarage_km']
            CarData.add_dataInt(new_car,6,avarage_km)
            db.session.commit()
            return jsonify(car_schema.dump(new_car))

    @cars.expect(parserId, parserUserId, parserPage)
    def get(self):
        '''get all car owned by a user or 1'''
        if  request.args.get('id_user'):
            id_user=request.args.get('id_user')
            #cars = Car.query.filter_by(id_user=id_user).all()
            page = request.args.get('page', 1 , type=int)
            cars_count = Car.query.count()
            pages= cars_count // app.config['PER_PAGE'] + (cars_count % app.config['PER_PAGE'] > 0)
            cars = Car.query.filter_by(id_user=id_user).paginate(page, app.config['PER_PAGE'], False).items
            response =   { "page": page, "per_page": app.config['PER_PAGE'],
                    "total": cars_count, "total_pages": pages, "data": []}
            response["data"]=cars_schema.dump(cars)
            return jsonify(response)
            if not cars:
                return 'car Not Found', 404
            return jsonify(cars_schema.dump(cars))
        elif request.args.get('car_id'):
            car_id=request.args.get('car_id')
            car = Car.query.get(car_id)
            if not car:
                return 'car Not Found', 404
            return jsonify(car_schema.dump(car))
        else:
            page = request.args.get('page', 1 , type=int)
            cars_count = Car.query.count()
            pages= cars_count // app.config['PER_PAGE'] + (cars_count % app.config['PER_PAGE'] > 0)
            cars = Car.query.paginate(page, app.config['PER_PAGE'], False).items
            response =   { "page": page, "per_page": app.config['PER_PAGE'],
                    "total": cars_count, "total_pages": pages, "data": []}
            response["data"]=cars_schema.dump(cars)
            return jsonify(response)

