from models import db
from flask import Blueprint
from utils.utils import get_response
from models.certificate import Certificate
from utils.decorators import login_required
from flask_restful import Api, Resource, reqparse

certificate_create_parse = reqparse.RequestParser()
certificate_create_parse.add_argument("title", type=str, required=True, help="Title cannot be blank")
certificate_create_parse.add_argument("description", type=str, required=True, help="Description cannot be blank")
certificate_create_parse.add_argument("file_path", type=str, required=True, help="File Path cannot be blank")

certificate_update_parse = reqparse.RequestParser()
certificate_update_parse.add_argument("title", type=str)
certificate_update_parse.add_argument("description", type=str)
certificate_update_parse.add_argument("file_path", type=str)

certificate_bp = Blueprint("certificate", __name__, url_prefix="/api/certificate")
api = Api(certificate_bp)

class CertificateResource(Resource):
    
    def get(self, certificate_id):
        """Certificate Get API
        Path - /api/certificate/<certificate_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - name: certificate_id
              in: path
              type: integer
              required: true
              description: Enter Certificate ID
        responses:
            200:
                description: Return a Certificate
            404:
                description: Certificate not found
        """
        certificate = Certificate.query.filter_by(id=certificate_id).first()
        if not certificate:
            return get_response("Certificate not found", None, 404), 404
        
        return get_response("Certificate successfully found", Certificate.to_dict(certificate), 200), 200

    @login_required()
    def delete(self, certificate_id):
        """Certificate Delete API
        Path - /api/certificate/<certificate_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication
              
            - name: certificate_id
              in: path
              type: integer
              required: true
              description: Enter Certificate ID
        responses:
            200:
                description: Delete a Certificate
            404:
                description: Certificate not found
        """
        certificate = Certificate.query.filter_by(id=certificate_id).first()
        if not certificate:
            return get_response("Certificate not found", None, 404), 404
        
        db.session.delete(certificate)
        db.session.commit()
        return get_response("Successfully deleted certificate", None, 200), 200
    
    @login_required()
    def patch(self, certificate_id):
        """Certificate Update API
        Path - /api/certificate/<certificate_id>
        Method - PATCH
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: certificate_id
              in: path
              type: integer
              required: true
              description: Enter Certificate ID

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
                    file_path:
                        type: string
        responses:
            200:
                description: Successfully updated certificate
            404:
                description: Certificate not found
        """
        found_certificate = Certificate.query.filter_by(id=certificate_id).first()
        if not found_certificate:
            return get_response("Certificate not found", None, 404), 404
        
        data = certificate_update_parse.parse_args()
        title = data.get('title', None)
        description = data.get('description', None)
        file_path = data.get('file_path', None)

        if title is not None:
            found_certificate.title = title
        if description is not None:
            found_certificate.description = description
        if file_path is not None:
            found_certificate.file_path = file_path
       
        db.session.commit()
        return get_response("Successfully updated certificate", None, 200), 200

class CertificateListCreateResource(Resource):

    def get(self):
        """Certificate List API
        Path - /api/certificate
        Method - GET
        ---
        consumes: application/json
        responses:
            200:
                description: Return Certificate List
        """
        certificate_list = Certificate.query.filter_by().order_by(Certificate.created_at.desc()).all()
        result_certificate_list = [Certificate.to_dict(certificate) for certificate in certificate_list]
        return get_response("Certificate List", result_certificate_list, 200), 200

    @login_required()
    def post(self):
        """Certificate Create API
        Path - /api/certificate
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
                    file_path:
                        type: string
                required: [title, description, file_path]
        responses:
            200:
                description: Return New Certificate ID
            400:
                description: Title, Description or File Path is Blank
        """
        data = certificate_create_parse.parse_args()
        title = data['title']
        description = data['description']
        file_path = data['file_path']
        
        new_certificate = Certificate(title, description, file_path)
        db.session.add(new_certificate)
        db.session.commit()
        return get_response("Successfully created certificate", new_certificate.id, 200), 200

api.add_resource(CertificateResource, "/<certificate_id>")
api.add_resource(CertificateListCreateResource, "/")
