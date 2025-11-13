from models import db
from flask import Blueprint
from models.contact import Contact
from utils.utils import get_response
from utils.decorators import login_required
from flask_restful import Api, Resource, reqparse

contact_parse = reqparse.RequestParser()
contact_parse.add_argument("full_name", type=str, required=True, help="Full Name cannot be blank")
contact_parse.add_argument("phone_number", type=str, required=True, help="Phone Number cannot be blank")
contact_parse.add_argument("subject", type=str, required=True, help="Subject cannot be blank")
contact_parse.add_argument("message", type=str, required=True, help="Message cannot be blank")

contact_bp = Blueprint("contact", __name__, url_prefix="/api/contact")
api = Api(contact_bp)

class ContactResource(Resource):
    decorators = [login_required()]

    def get(self, contact_id):
        """Contact Get API
        Path - /api/contact/<contact_id>
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

            - name: contact_id
              in: path
              type: integer
              required: true
              description: Enter Contact ID
        responses:
            200:
                description: Return a Contact
            404:
                description: Contact not found
        """
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return get_response("Contact not found", None, 404), 404
        
        return get_response("Contact successfully found", Contact.to_dict(contact), 200), 200

    def delete(self, contact_id):
        """Contact Delete API
        Path - /api/contact/<contact_id>
        Method - DELETE
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication
              
            - name: contact_id
              in: path
              type: integer
              required: true
              description: Enter Contact ID
        responses:
            200:
                description: Delete a Contact
            404:
                description: Contact not found
        """
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return get_response("Contact not found", None, 404), 404
        
        db.session.delete(contact)
        db.session.commit()
        return get_response("Successfully deleted contact", None, 200), 200

class ContactListCreateResource(Resource):

    @login_required()
    def get(self):
        """Contact List API
        Path - /api/contact
        Method - GET
        ---
        consumes: application/json
        parameters:
            - in: header
              name: Authorization
              type: string
              required: true
              description: Bearer token for authentication

        responses:
            200:
                description: Return Contact List
        """
        contact_list = Contact.query.filter_by().order_by(Contact.created_at.desc()).all()
        result_contact_list = [Contact.to_dict(contact) for contact in contact_list]
        return get_response("Contact List", result_contact_list, 200), 200
    
    def post(self):
        """Contact Create API
        Path - /api/contact
        Method - POST
        ---
        consumes: application/json
        parameters:
            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                    full_name: 
                        type: string
                    phone_number:
                        type: string
                    subject:
                        type: string
                    message:
                        type: string
                required: [full_name, phone_number, subject, message]
        responses:
            200:
                description: Return New Contact ID
            400:
                description: Full Name, Phone Number, Subject or Message is Blank
        """
        data = contact_parse.parse_args()
        full_name = data['full_name']
        phone_number = data['phone_number']
        subject = data['subject']
        message = data['message']
        
        new_contact = Contact(full_name, phone_number, subject, message)
        db.session.add(new_contact)
        db.session.commit()
        return get_response("Successfully created contact", new_contact.id, 200), 200

api.add_resource(ContactResource, "/<contact_id>")
api.add_resource(ContactListCreateResource, "/")
