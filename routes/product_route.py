from models import db
from flask import Blueprint
from models.product import Product
from utils.utils import get_response
from utils.decorators import login_required
from flask_restful import Api, Resource, reqparse

product_create_parse = reqparse.RequestParser()
product_create_parse.add_argument("title", type=str, required=True, help="Title cannot be blank")
product_create_parse.add_argument("description", type=str, required=True, help="Description cannot be blank")
product_create_parse.add_argument("image_path", type=str, required=True, help="Image Path cannot be blank")
product_create_parse.add_argument("proba", type=int, required=True, help="Proba cannot be blank")
product_create_parse.add_argument("gramm", type=float, required=True, help="Gramm cannot be blank")
product_create_parse.add_argument("type", type=str, required=True, help="Type cannot be blank")

product_update_parse = reqparse.RequestParser()
product_update_parse.add_argument("title", type=str)
product_update_parse.add_argument("description", type=str)
product_update_parse.add_argument("image_path", type=str)
product_update_parse.add_argument("proba", type=int)
product_update_parse.add_argument("gramm", type=float)
product_update_parse.add_argument("type", type=str)

product_bp = Blueprint("product", __name__, url_prefix="/api/product")
api = Api(product_bp)

class ProductResource(Resource):
    
    def get(self, product_id):
        """Product Get API
        Path - /api/product/<product_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - name: product_id
              in: path
              type: integer
              required: true
              description: Enter Product ID
        responses:
            200:
                description: Return a Product
            404:
                description: Product not found
        """
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return get_response("Product not found", None, 404), 404
        
        return get_response("Product successfully found", Product.to_dict(product), 200), 200

    @login_required()
    def delete(self, product_id):
        """Product Delete API
        Path - /api/product/<product_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication
              
            - name: product_id
              in: path
              type: integer
              required: true
              description: Enter Product ID
        responses:
            200:
                description: Delete a Product
            404:
                description: Product not found
        """
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return get_response("Product not found", None, 404), 404
        
        db.session.delete(product)
        db.session.commit()
        return get_response("Successfully deleted product", None, 200), 200
    
    @login_required()
    def patch(self, product_id):
        """Product Update API
        Path - /api/product/<product_id>
        Method - PATCH
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: product_id
              in: path
              type: integer
              required: true
              description: Enter Product ID

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    title: 
                        type: string
                    description:
                        type: string
                    image_path:
                        type: string
                    proba:
                        type: integer
                    gramm:
                        type: float
                    type:
                        type: string
        responses:
            200:
                description: Successfully updated product
            404:
                description: Product not found
        """
        found_product = Product.query.filter_by(id=product_id).first()
        if not found_product:
            return get_response("Product not found", None, 404), 404
        
        data = product_update_parse.parse_args()
        title = data.get('title', None)
        description = data.get('description', None)
        image_path = data.get('image_path', None)
        proba = data.get('proba', None)
        gramm = data.get('gramm', None)
        type = data.get('type', None)

        if title is not None:
            found_product.title = title
        if description is not None:
            found_product.description = description
        if image_path is not None:
            found_product.image_path = image_path
        if proba is not None:
            found_product.proba = proba
        if gramm is not None:
            found_product.gramm = gramm
        if type is not None:
            found_product.type = type
       
        db.session.commit()
        return get_response("Successfully updated product", None, 200), 200

class ProductListCreateResource(Resource):

    def get(self):
        """Product List API
        Path - /api/product
        Method - GET
        ---
        consumes: application/json
        responses:
            200:
                description: Return Product List
        """
        product_list = Product.query.filter_by().order_by(Product.created_at.desc()).all()
        result_product_list = [Product.to_dict(product) for product in product_list]
        return get_response("Product List", result_product_list, 200), 200

    @login_required()
    def post(self):
        """Product Create API
        Path - /api/product
        Method - POST
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    title: 
                        type: string
                    description:
                        type: string
                    image_path:
                        type: string
                    proba:
                        type: integer
                    gramm:
                        type: float
                    type:
                        type: string
                required: [title, description, image_path, proba, gramm, type]
        responses:
            200:
                description: Return New Product ID
            400:
                description: Title, Description, Image Path, Proba, Gramm or Type is Blank
        """
        data = product_create_parse.parse_args()
        title = data['title']
        description = data['description']
        image_path = data['image_path']
        proba = data['proba']
        gramm = data['gramm']
        type = data['type']
        
        new_product = Product(title, description, image_path, proba, gramm, type)
        db.session.add(new_product)
        db.session.commit()
        return get_response("Successfully created product", new_product.id, 200), 200

api.add_resource(ProductResource, "/<product_id>")
api.add_resource(ProductListCreateResource, "/")
