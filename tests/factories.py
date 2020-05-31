# -*- coding: utf-8 -*-
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.extensions import db
import app.models as m


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.User
        sqlalchemy_session = db.session
    id = factory.Sequence(lambda n: f'user_{n}')
    name = factory.Sequence(lambda n: f'User {n}')
    email = factory.Sequence(lambda n: f'user{n}@email.com')
    phone_number = factory.Sequence(
        lambda n: '0' * (10 - len(str(n))) + str(n))


class OAuth2ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.OAuth2Client
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    client_id = factory.Sequence(lambda n: f'client_id_{n}')
    client_secret = factory.Sequence(lambda n: f'client_secret_{n}')
    redirect_uri = factory.Sequence(lambda n: f'http://client{n}.example.com')
    token_endpoint_auth_method = 'client_secret_post'
    grant_type = 'authorization_code'
    response_type = 'code'
    scope = 'openid profile'
    client_name = factory.Sequence(lambda n: f'Test Client {n}')
    user = factory.SubFactory(UserFactory)


class ScopeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Scope
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    scope = factory.Sequence(lambda n: f'scope_{n}')
    is_default = False
    description = factory.Faker('text')


class ServiceGroupFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.ServiceGroup
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'service_group_name_{n+1}')
    code = factory.Sequence(lambda n: f'service_group_code_{n+1}')


class ServiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Service
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'name_{n+1}')
    code = factory.Sequence(lambda n: f'code_{n+1}')
    service_info = factory.Sequence(lambda n: f'service_info_{n+1}')
    service_metadata = factory.Sequence(lambda n: f'service_metadata_{n+1}')
    public_url = factory.Sequence(lambda n: f'public_url_{n+1}')
    private_url = factory.Sequence(lambda n: f'private_url_{n+1}')
    is_active = 1

    service_group = factory.SubFactory(ServiceGroupFactory)


class ResourceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Resource
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'name_{n+1}')
    code = factory.Sequence(lambda n: f'code_{n+1}')
    is_active = 1

    service = factory.SubFactory(ServiceFactory)


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Role
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'name_{n+1}')
    code = factory.Sequence(lambda n: f'code_{n+1}')

    service = factory.SubFactory(ServiceFactory)


class ActionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Action
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'name_{n+1}')
    code = factory.Sequence(lambda n: f'code_{n+1}')


class PermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Permission
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f'name_{n+1}')
    code = factory.Sequence(lambda n: f'code_{n+1}')

    resource = factory.SubFactory(ResourceFactory)
    action = factory.SubFactory(ActionFactory)


class RouteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = m.Route
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    reg_uri = factory.Sequence(lambda n: f'reg_uri_{n+1}')
    name = factory.Sequence(lambda n: f'name_{n+1}')
    method = 'GET'

    required_permission = factory.SubFactory(PermissionFactory)
    resource = factory.SubFactory(ResourceFactory)
