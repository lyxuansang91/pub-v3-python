# -*- coding: utf-8 -*-
# import json


# import requests
# from flask import Blueprint, current_app, g, request
from flask import Blueprint

from app import models as m  # noqa
from app.extensions import api  # noqa

from .adv import ns as adv_ns
from .category import ns as category_ns
from .conversion import ns as conversion_ns
from .offer import ns as offer_ns
# import jwt
from .user import ns as user_ns
from .domain import ns as domain_ns

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')

api.add_namespace(ns=user_ns)
api.add_namespace(ns=category_ns)
api.add_namespace(ns=adv_ns)
api.add_namespace(ns=offer_ns)
api.add_namespace(ns=conversion_ns)
api.add_namespace(ns=domain_ns)
