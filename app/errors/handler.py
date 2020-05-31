from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException
from .exceptions import ApiException


def api_error_handler(error):
    if isinstance(error, ApiException):
        current_app.logger.warning(f'ApiException: {error.status_code} - {error.to_dict}')
        return jsonify(error.to_dict), error.status_code
    elif isinstance(error, HTTPException):
        current_app.logger.warning(f'HTTPException: {error.code} - {error.description}')
        return jsonify({'error': {'code': error.code, 'message': error.description}}), error.code
    else:
        current_app.logger.error(error)
        return jsonify({'error': {'code': 500, 'message': 'Internal Server Error'}}), 500
