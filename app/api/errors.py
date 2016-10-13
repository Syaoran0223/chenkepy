# coding: utf-8

from flask import jsonify
from app.exceptions import ValidationError
from . import api_blueprint


def bad_request(message):
    response = jsonify({'status': 'Bad Request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message='Unauthorized Access'):
    response = jsonify({'status': 'Unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'status': 'Forbidden', 'message': message})
    response.status_code = 403
    return response


@api_blueprint.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

@api_blueprint.app_errorhandler(JsonOutputException)
def json_output(e):
    response = jsonify({'code': '400', 'msg': str(e)})
    response.status_code = 200
    return response
