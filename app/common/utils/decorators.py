from flask import current_app, request


def allowed_ip(func):

    def wrapper(*args, **kwargs):

        if request.remote_addr in current_app.config["ALLOW_HOST"]:

            return func(*args, **kwargs)

        else:

            return {'message': 'Your IP is not allowed to send email using bot.'}, 401

    return wrapper
