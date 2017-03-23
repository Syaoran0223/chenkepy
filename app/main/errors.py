from flask import render_template, request, jsonify
from app.exceptions import JsonOutputException, FormValidateError, AdminException
from . import main

@main.app_errorhandler(404)
def page_no_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'status': 'Not Found', 'message': 'not found'})
        response.status_code = 404
        return response
    return render_template('commons/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'status': 'Internal Server Error', 'message': 'server error'})
        response.status_code = 500
        return response
    return render_template('commons/500.html'), 500

@main.app_errorhandler(JsonOutputException)
def json_output(e):
    response = jsonify({'code': '400', 'msg': str(e)})
    response.status_code = 200
    return response

@main.app_errorhandler(FormValidateError)
def form_validate(e):
    msg = ''
    if (len(e.args) > 0):
        msg_origin = e.args[0]
        for (key, value) in msg_origin.items():
            for err in value:
                msg += err + ' '
            msg += key
    response = jsonify({'code': '400', 'msg': msg})
    response.status_code = 200
    return response

@main.app_errorhandler(AdminException)
def admin_error(e):
    response = jsonify({'msg': str(e)})
    response.status_code = 400
    return response
