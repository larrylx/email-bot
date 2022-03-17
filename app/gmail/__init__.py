from flask import Blueprint
from flask_restful import Api

from . import gmail
from app.common.utils.output_json import output_json

gmail_api_bp = Blueprint('GmailApi', __name__, url_prefix='/gmailapi')
gmail_api = Api(gmail_api_bp, catch_all_404s=True)
gmail_api.representation('application/json')(output_json)

gmail_api.add_resource(gmail.GmailBot, '/noattachment', endpoint='Send_Email_Without_Attachment')
