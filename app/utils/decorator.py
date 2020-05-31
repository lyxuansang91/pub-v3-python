# -*- coding: utf-8 -*-
from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError

from app.errors.exceptions import (BadRequest, Unauthorized,
                                   UnSupportedMediaType, NotFound)
from ..repositories import user_repo


def consumes(*content_types):
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.mimetype not in content_types:
                raise UnSupportedMediaType(message='Unsupported media type')
            return func(*args, **kwargs)
        return wrapper
    return decorated


def authorized():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            headers = request.headers.get('Authorization')
            if headers is None:  # do not have authorization header, process as a signup user
                new_args = args + (None, )
                return func(*new_args, **kwargs)
            authorization_type = headers.split(' ')[0]
            if authorization_type != 'Bearer':
                raise Unauthorized(code=401, message='Token Type is not valid')
            current_user_id = get_jwt_identity()
            user = user_repo.find_by_id(current_user_id)
            if user is None:
                raise NotFound(code=404, message='User is not found')
            if not user.active:
                raise BadRequest(code=400, message='User is not active')
            new_args = args + (user, )
            return func(*new_args, **kwargs)
        return wrapper
    return decorated


def admin_required():
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            headers = request.headers.get('Authorization')
            if headers is None:  # do not have authorization header, process as a signup user
                new_args = args + (None, )
                return func(*new_args, **kwargs)
            authorization_type = headers.split(' ')[0]
            if authorization_type != 'Bearer':
                raise Unauthorized(code=401, message='Token Type is not valid')
            current_user_id = get_jwt_identity()
            user = user_repo.find_by_id(current_user_id)
            if user is None:
                raise NotFound(code=404, message='User is not found')
            if not user.active:
                raise BadRequest(code=400, message='User is not active')
            new_args = args + (user, )
            return func(*new_args, **kwargs)
        return wrapper
    return decorated


def use_args(**schema):
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req_args = request.args.to_dict()
            if request.method in ('POST', 'PUT', 'PATCH', 'DELETE') \
                    and request.mimetype == 'application/json':
                req_args.update(request.get_json())
            req_args = {k: v for k, v in req_args.items(
            ) if k in schema['properties'].keys()}
            if 'required' in schema:
                for field in schema['required']:
                    if field not in req_args or not req_args[field]:
                        field_name = field
                        if field in schema['properties']:
                            if 'name' in schema['properties'][field]:
                                field_name = schema['properties'][field]['name']
                        raise BadRequest(message='{} is required'.format(field_name))
            try:
                validate(instance=req_args, schema=schema,
                         format_checker=FormatChecker())
            except ValidationError as exp:
                exp_info = list(exp.schema_path)
                error_type = ('type', 'format', 'pattern',
                              'maxLength', 'minLength')
                if set(exp_info).intersection(set(error_type)):
                    field = exp_info[1]
                    field_name = field
                    if field_name in schema['properties']:
                        if 'name' in schema['properties'][field]:
                            field_name = schema['properties'][field]['name']
                    message = '{} is not valid'.format(field_name)
                else:
                    message = exp.message  # pragma: no cover
                raise BadRequest(message=message)
            new_args = args + (req_args, )
            return func(*new_args, **kwargs)
        return wrapper
    return decorated
