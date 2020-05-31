# -*- coding: utf-8 -*-
import enum
import uuid
from datetime import datetime
from threading import Thread  # noqa

import requests
from flask import current_app, g
from app.repositories import postback_log_repo


def send_async_request(app, user, conversion):

    with app.app_context():
        from app.models import PostbackLogStatus
        status = PostbackLogStatus.SUCCESS
        postback_url = generate_url_from_postback_url(user.postback_url)
        try:
            response = requests.get(postback_url)
            status = PostbackLogStatus.SUCCESS if response.status_code == 200 else PostbackLogStatus.FAILED
            raw_response = response.text
        except Exception as e:
            raw_response = str(e)
            status = PostbackLogStatus.ERROR
        finally:
            args = {
                'user_id': str(user.id),
                'order_id': str(conversion.order_id),
                'offer_id': str(conversion.offer_id),
                'url': postback_url,
                'raw_url': user.postback_url,
                'raw_response': raw_response,
                'status': status,
            }
            postback_log_repo.create_from_args(args)


def send_request(user, conversion=None):
    def generate_url_from_postback_url(url):
        new_url = url.replace("{order_id}", str(conversion.order_id)).replace("{offer_id}", str(conversion.offer_id)).replace(
            "{status}", conversion.status.value).replace("{aff_sub1}", str(conversion.order_id)).replace(
            "{name}", conversion.name).replace("{phone}", conversion.phone).replace("{msg}", conversion.name)
        return new_url

    from app.models import PostbackLogStatus

    status = PostbackLogStatus.SUCCESS
    postback_url = generate_url_from_postback_url(user.postback_url)
    try:
        response = requests.get(postback_url)
        status = PostbackLogStatus.SUCCESS if response.status_code == 200 else PostbackLogStatus.FAILED
        raw_response = response.text
    except Exception as e:
        raw_response = str(e)
        status = PostbackLogStatus.ERROR
    finally:
        args = {
            'user_id': str(user.id),
            'order_id': str(conversion.order_id),
            'offer_id': str(conversion.offer_id),
            'url': postback_url,
            'raw_url': user.postback_url,
            'raw_response': raw_response,
            'status': status,
        }
        postback_log_repo.create_from_args(args)


def get_model_value(val):
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(val, enum.Enum):
        return val.value
    if isinstance(val, uuid.UUID):
        return str(val)
    return val


def get_model_value_primitive(val):
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def get_current_user():
    return getattr(g, 'user_id', None)
