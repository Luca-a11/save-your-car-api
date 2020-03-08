from flask import jsonify, request
from flask_restplus import Resource, reqparse, fields
from app.users.models import User, UserSchema
from app import api
from app import db
from app import app

users = api.namespace('api/v1.0/users',description='CRUD operation for syc users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

userModel = users.model('userModel', {
    'username' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True),
    'password': fields.String(validate=True),
    'image_file' : fields.String(validate=True)
})

parserId = reqparse.RequestParser()
parserId.add_argument('user_id',type=int)

parserPage = reqparse.RequestParser()
parserPage.add_argument('page',type=int, default=1)

@users.route('/<string:email>/<string:password>')
class GET_User(Resource):
    def get(self,email,password):
        '''get user by matching usrname and password'''
        user = User.query.filter_by(email=email).first()
        if not user:
           return 'User Not Found', 404
        elif user.password != password:
           return 'Wrong Password', 400
        return jsonify(user_schema.dump(user))

@users.route('/<int:user_id>')
class Requests_UserById(Resource):
    def get(self,user_id):
        '''get a user by id'''
        user = User.query.get(user_id)
        if not user:
            return 'User Not Found', 404
        return jsonify(user_schema.dump(user))

    @users.expect(userModel, validate=True)
    def put(self,user_id):
        '''update user data'''
        user = User.query.get(user_id)
        if not user:
           return 'User Not Found', 404
        print(request.get_json())
        user.username = request.get_json()['username'] if request.get_json()['username'] else user.username
        user.password = request.get_json()['password'] if request.get_json()['password'] else user.password
        user.image_file =  request.get_json()['image_file'] if request.get_json()['image_file'] else user.image_file
        user.email =  request.get_json()['email'] if request.get_json()['email'] else user.email
        db.session.commit()
        return jsonify(user_schema.dump(user))

    def delete(self,user_id):
        '''delete a user'''
        try:
            user = User.query.get(user_id)
            if not user:
             return 'User Not Found', 404
            db.session.delete(user)
            db.session.commit()
            return jsonify({'result': True})
        except:
            return 'Error Server Side', 500

@users.route('')
class General_Users_Requests(Resource):
    @users.expect(userModel, validate=True)
    def post(self):
            '''Register a user'''
            username = request.get_json()['username'] 
            password = request.get_json()['password']
            image_file =  request.get_json()['image_file'] 
            email =  request.get_json()['email']
            new_user = User(
            username=username,
            email=email,
            image_file=image_file,
            password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(user_schema.dump(new_user))

    @users.expect(parserId, parserPage)
    def get(self):
        '''get all users or 1'''
        if request.args.get('user_id'):
            user_id=request.args.get('user_id')
            user = User.query.get(user_id)
            if not user:
                return 'User Not Found', 404
            return jsonify(user_schema.dump(user))
        else:
            page = request.args.get('page', 1 , type=int)
            users_count = User.query.count()
            pages= users_count // app.config['PER_PAGE'] + (users_count % app.config['PER_PAGE'] > 0)
            users = User.query.paginate(page, app.config['PER_PAGE'], False).items
            response =   { "page": page, "per_page": app.config['PER_PAGE'],
                    "total": users_count, "total_pages": pages, "data": []}
            response["data"]=users_schema.dump(users)
            return jsonify(response)