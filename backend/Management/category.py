from flask import Blueprint,jsonify,request
from flask_restful import Api,Resource,reqparse
from model import db,Category

category_bp = Blueprint('category_bp',__name__)

api = Api(category_bp)


class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()

        return jsonify([{
            'id':category.id,
            'name':category.name
        } for category in categories])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True)

        args = parser.parse_args()

        if Category.query.filter_by(name=args['name']).first():
            return {"message":"Category already exists"},400
        new_category=Category(name=args['name'])
        db.session.add(new_category)
        db.session.commit()

        return {"message":"Category Created Succesfully"}, 200
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True,help='Category Id is required')
        parser.add_argument('name',type=str,required=True)

        args = parser.parse_args()

        category = Category.query.get(args['id'])

        if not category:
            return {"message":"category not found"},404
        
        category.name = args['name']
        db.session.commit()

        return {"message":"Category updated successfully"},200
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int,required=True,help='Category Id is required')

        args = parser.parse_args()

        category = Category.query.get(args['id'])

        if not category:
            return {"message":"category not found"},404
        
        db.session.delete(category)
        db.session.commit()

        return {"message":"Category deleted Successfully"},200
    
api.add_resource(CategoryResource,'/category')