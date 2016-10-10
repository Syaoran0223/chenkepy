from flask import render_template, request, jsonify
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