from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

import base64
import json

from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.common.utils import email_parser
from app.common.utils.decorators import allowed_ip


class GmailBot(Resource):
    method_decorators = [allowed_ip]

    def __init__(self):
        self.delegated_user = current_app.config["GOOGLE_WORKSPACE_USER"]
        if not self.delegated_user:
            raise ValueError("No GOOGLE_WORKSPACE_USER is set for Environment Variable")

        self.credentials_json = json.loads(current_app.config["GOOGLE_WORKSPACE_SERVICE_ACCOUNT_CREDENTIALS"])
        if not self.credentials_json:
            raise ValueError("No GOOGLE_WORKSPACE_SERVICE_ACCOUNT_CREDENTIALS_JSON_STR is set for Environment Variable")

        self.scopes = ['https://www.googleapis.com/auth/gmail.send']

    def _service_account_login(self):
        credentials = service_account.Credentials.from_service_account_info(self.credentials_json, scopes=self.scopes)
        delegated_credentials = credentials.with_subject(self.delegated_user)
        service = build('gmail', 'v1', credentials=delegated_credentials)
        return service

    def _create_message(self, to, subject, message_text):
        """Create a message for an email.
        Args:
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
        Returns:
            An object containing a base64url encoded email object.
        """
        sender = current_app.config["SEND_AS"]
        if not sender:
            sender = self.delegated_user

        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        b64_string = b64_bytes.decode()
        return {'raw': b64_string}

    def post(self):
        """Send an email message.
        Returns:
            Sent Message.
        """
        parser = RequestParser()
        parser.add_argument('to', type=email_parser.email, required=True, location='json')
        parser.add_argument('subject', required=True, location='json')
        parser.add_argument('message', required=True, location='json')
        args = parser.parse_args()
        to = args.to
        subject = args.subject
        body = args.message
        try:
            message = (self._service_account_login().users().messages().send(userId="me",
                                                                             body=self._create_message(
                                                                                 to,
                                                                                 subject,
                                                                                 body
                                                                             )).execute())
            return message
        except HttpError as error:
            return {'message': error}, 500


class EmailAttachment(Resource):
    def post(self):
        pass
