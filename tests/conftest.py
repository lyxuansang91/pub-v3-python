# -*- coding: utf-8 -*-
import pytest
from docstring_parser import parse
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers

from app import create_app
from app.extensions import db

from . import factories as f
from .services import jira_test_service


@pytest.fixture(scope='session')
def app():
    app = create_app(environment='testing')
    with app.app_context():
        yield app
        db.drop_all()
        db.session.remove()


@pytest.fixture(autouse=True)
def database(app):
    db.create_all()
    db.session.commit()
    yield
    db.drop_all()
    db.session.remove()


@pytest.fixture
def token(app):
    return access_token()


def access_token():
    return """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imlzcy1odHRwczovL2Rldi1pZC50ZWtvLnZuLyJ9.eyJqdGkiOiJjUVVJM1p3RFJNTjhrdkJNN2plaDV3dVgiLCJzdWIiOiIwYjUxMTIyZWEwM2Q0M2ViYThkNDY2YTJkM2MzZWVhMiIsImlzcyI6Imh0dHBzOi8vZGV2LWlkLnRla28udm4vIiwiYXVkIjoiYTM5M2I2MzkyYzMxNDkzZTkxYjMyM2U0NDk5ZGNiZTciLCJpYXQiOjE1NjgzNTg0NTAsImV4cCI6MTU2OTIyMjQ1MCwic2NvcGUiOiIifQ.TIwRefu5vY6C-3gSFvkBJpaABHq0d9Ha0tH-rndT0g6qPwBX8EfXydLgeVAhjY8l2SU-K-0RkS42PYUjP4oHDTAdnLnv-WhUKdOmiSmAm_OjMm-AQussmg5f28v0739wNsQskZHDcWQKUGxitjjq-KGOrSqI2GzuBHLpPc2jrtEU5qudQy_bE-_JFoBdrDX5mEe1v5amX87Yn4ICO_xb7O4kUKMLo_4y3RH5z_ZgFvssEuQ9m6p5KBnO_XzmnYmqd3n_1ksSj8ZIa6LPozE2LszLQzma2BXQ_n3cEMMTF9IH0NNMCIKOVeH4EoeSnJc-NEjBqlrOFZHr7hm05vrt0g"""


@pytest.fixture
def client(app):
    app.test_client_class = CustomClient
    client = app.test_client()
    return client


@pytest.fixture
def user(app):
    user = f.UserFactory()
    db.session.commit()
    return user


@pytest.fixture
def make_user(app):
    def wrapper(user_id):
        user = f.UserFactory(id=user_id)
        db.session.commit()
        return user
    return wrapper


@pytest.fixture
def scope(app):
    scope = f.ScopeFactory()
    db.session.commit()
    return scope


@pytest.fixture
def make_scopes(app):
    def wrapper(size):
        scopes = f.ScopeFactory.create_batch(size)
        db.session.commit()
        return scopes

    return wrapper


class CustomClient(FlaskClient):
    def open(self, *args, **kwargs):
        authorization_headers = Headers({'Authorization': 'Bearer ' + access_token()})
        headers = kwargs.pop('headers', Headers())
        kwargs['headers'] = {**authorization_headers, **headers}
        return super().open(*args, **kwargs)


class ClientFactory(object):
    def __init__(self, user):
        self._user = user

    def confidential_client(self,
                            grant_type='authorization_code',
                            response_type='code',
                            token_endpoint_auth_method='client_secret_basic',
                            scope='openid profile'):

        client = f.OAuth2ClientFactory(
            user=self._user,
            grant_type=grant_type,
            response_type=response_type,
            token_endpoint_auth_method=token_endpoint_auth_method,
            scope=scope)
        db.session.commit()
        return client

    def public_client(self,
                      grant_type='authorization_code',
                      response_type='code',
                      scope='openid profile'):
        client = f.OAuth2ClientFactory(user=self._user,
                                       grant_type=grant_type,
                                       response_type=response_type,
                                       token_endpoint_auth_method='none',
                                       client_secret='',
                                       scope=scope)
        db.session.commit()
        return client

    def credentials_client(self, scope='openid profile'):
        client = f.OAuth2ClientFactory(
            user=self._user,
            grant_type='client_credentials',
            response_type='code',
            token_endpoint_auth_method='client_secret_basic',
            scope=scope)
        db.session.commit()
        return client

    def password_client(self, scope='openid profile'):
        client = f.OAuth2ClientFactory(
            user=self._user,
            grant_type='password',
            response_type='code',
            token_endpoint_auth_method='client_secret_basic',
            scope=scope)
        db.session.commit()
        return client

    def implicit_client(self, scope='openid profile'):
        client = f.OAuth2ClientFactory(user=self._user,
                                       response_type='token',
                                       token_endpoint_auth_method='none',
                                       client_secret='',
                                       grant_type='',
                                       scope=scope)
        db.session.commit()
        return client


@pytest.fixture
def client_factory(user):
    return ClientFactory(user)


class ServiceGroupFactory(object):
    def create(self):
        service_group = f.ServiceGroupFactory()
        db.session.commit()
        return service_group


@pytest.fixture
def service_group_factory():
    return ServiceGroupFactory()


@pytest.fixture
def service_group_instance():
    return ServiceGroupFactory().create()


class ServiceFactory(object):
    def create(self, service_group):
        service = f.ServiceFactory(service_group=service_group)
        db.session.commit()
        return service


@pytest.fixture
def service_factory():
    return ServiceFactory()


@pytest.fixture
def service_instance(service_group_instance):
    return ServiceFactory().create(service_group_instance)


class ActionFactory(object):
    def create(self):
        action = f.ActionFactory()
        db.session.commit()
        return action


@pytest.fixture
def action_factory():
    return ActionFactory()


@pytest.fixture
def action_instance():
    return ActionFactory().create()


class ResourceFactory(object):
    def create(self, service):
        resource = f.ResourceFactory(service=service)
        db.session.commit()
        return resource


@pytest.fixture
def resource_factory():
    return ResourceFactory()


@pytest.fixture
def resource_instance(service_instance):
    return ResourceFactory().create(service_instance)


class PermissionFactory(object):
    def create(self, resource, action):
        permission = f.PermissionFactory(resource=resource, action=action)
        db.session.commit()
        return permission


@pytest.fixture
def permission_factory():
    return PermissionFactory()


@pytest.fixture
def permission_instance(resource_instance, action_instance):
    return PermissionFactory().create(resource_instance, action_instance)


class RouteFactory(object):
    def create(self, permission, resource):
        route = f.RouteFactory(required_permission=permission,
                               resource=resource)
        db.session.commit()
        return route


@pytest.fixture
def route_factory():
    return RouteFactory()


class RoleFactory(object):
    def create(self, service):
        role = f.RoleFactory(service=service)
        db.session.commit()
        return role


@pytest.fixture
def role_factory():
    return RoleFactory()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    item.test_outcome = outcome.get_result()


def pytest_addoption(parser):
    parser.addoption('--submit-tests',
                     action='store_true',
                     help='Submit tests to Jira')


_tests = dict()


@pytest.fixture(scope='session', autouse=True)
def after_each_test_run(request):
    yield

    if request.config.getoption('--submit-tests'):
        test_service = jira_test_service()
        for issue_key in _tests.keys():
            # If the issue is closed, we don't need to submit the tests.
            issue = test_service.get_issue_info(issue_key)
            if issue['fields']['status']['name'] == 'Closed':
                continue
            # First, delete all tests associate with this issue key on TSM.
            tests = test_service.get_tests_in_issue(issue_key)
            for _, test_key in tests:
                test_service.delete_test(test_key)

            # Second, for each tests have found by pytest,
            # associate with this issue key, create and update its testCaseKey.
            for test in _tests[issue_key]:
                test_key = test_service.create_test(issue_key, test)
                test['testCaseKey'] = test_key

            # Last, create a test cycle for current issue key on TSM.
            cycle_items = [{
                key: item[key]
                for key in ['testCaseKey', 'status']
            } for item in _tests[issue_key]]
            test_service.create_test_cycle(issue_key, issue_key, cycle_items)


@pytest.fixture(autouse=True)
def after_each_test_case(request):
    yield

    docstring = parse(request._pyfuncitem._obj.__doc__)
    STEP_STRING = 'Step by step:'
    if docstring.long_description and STEP_STRING in docstring.long_description:
        objective, steps = map(
            str.strip, docstring.long_description.split(STEP_STRING, 1))
        steps = '<pre>' + steps + '</pre>'
    else:
        objective = docstring.long_description
        steps = None

    name = (docstring.short_description or request._pyfuncitem.name)[:255]
    status = 'Fail' if request.node.test_outcome.failed else 'Pass'

    cls_issue_key = request.cls and getattr(request.cls, 'ISSUE_KEY', None)
    # TODO: Each test case can have some addition issue keys.
    func_issue_keys = []
    issue_keys = [cls_issue_key] + func_issue_keys
    issue_keys = [item for item in issue_keys if item is not None]

    for issue_key in issue_keys:
        if not _tests.get(issue_key):
            _tests[issue_key] = []
        _tests[issue_key].append({
            'name': name,
            'objective': objective,
            'testScript': {
                'type': 'PLAIN_TEXT',
                'text': steps
            },
            'status': status
        })
