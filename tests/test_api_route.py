import json


class TestResourceApi():
    ISSUE_KEY = 'IAM-108'
    CLIENTS_ROUTE_ENDPOINT = '/api/v1.0/routes'

    def test_create_route_successfully(self, client, resource_instance):
        resource_id = resource_instance.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': resource_id
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 201

        data = response.json
        assert data['item']['reg_uri'] == route_body['reg_uri']
        assert data['item']['method'] == route_body['method']

    def test_create_route_400_route_reg_uri_required(self, client, resource_instance):
        resource_id = resource_instance.id

        route_body = {
            'reg_uri': '',
            'method': 'GET',
            'resource_id': resource_id
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 400

    def test_create_route_400_route_code_required(self, client, resource_instance):
        resource_id = resource_instance.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': '',
            'resource_id': resource_id
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 400

    def test_create_route_400_resource_id_required(self, client):
        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': None
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 400

    def test_create_route_404_resource_id(self, client):
        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': 999
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 404

    def test_create_route_404_permission_id(self, client, resource_instance):
        resource_id = resource_instance.id
        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': resource_id,
            'required_permission_id': 999
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 404

    def test_create_route_400_permission_not_for_resource(self, client, service_instance, resource_factory, permission_factory, action_instance):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]

        permissions = [permission_factory.create(resources[0], action_instance),
                       permission_factory.create(resources[1], action_instance)]

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': resources[0].id,
            'required_permission_id': permissions[1].id
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 400

    def test_create_route_400_route_existed(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        resource_id = resource_instance.id

        route_body = {
            'reg_uri': route.reg_uri,
            'method': route.method,
            'resource_id': resource_id
        }
        response = client.post(f'{self.CLIENTS_ROUTE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(route_body))

        assert response.status_code == 400

    def test_update_patch_route_successfully(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        route_id = route.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
        }
        response = client.patch(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(route_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['reg_uri'] == route_body['reg_uri']
        assert data['item']['method'] == route_body['method']

    def test_update_put_route_successfully(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        route_id = route.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['reg_uri'] == route_body['reg_uri']
        assert data['item']['method'] == route_body['method']

    def test_update_put_route_404_route_id(self, client):
        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/999',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 404

    def test_update_put_route_404_resource_id(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        route_id = route.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': 999
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 404

    def test_update_put_route_404_permission_id(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        route_id = route.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': resource_instance.id,
            'required_permission_id': 999
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 404

    def test_update_put_route_400_permission_not_for_resource(
            self, client, service_instance, resource_factory, permission_factory, route_factory, action_instance):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]

        permissions = [permission_factory.create(resources[0], action_instance),
                       permission_factory.create(resources[1], action_instance)]

        route = route_factory.create(permissions[0], resources[0])
        route_id = route.id

        route_body = {
            'reg_uri': 'reg_uri_0',
            'method': 'GET',
            'resource_id': resources[0].id,
            'required_permission_id': permissions[1].id
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 400

    def test_update_put_route_400_route_existed(self, client, permission_instance, resource_instance, route_factory):
        routes = [route_factory.create(permission_instance, resource_instance),
                  route_factory.create(permission_instance, resource_instance)]
        route_id = routes[0].id

        route_body = {
            'reg_uri': routes[1].reg_uri,
            'method': routes[1].method,
        }
        response = client.put(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(route_body))

        assert response.status_code == 400

    def test_delete_route_successfully(self, client, permission_instance, resource_instance, route_factory):
        route = route_factory.create(permission_instance, resource_instance)
        route_id = route.id

        response = client.delete(f'{self.CLIENTS_ROUTE_ENDPOINT}/{route_id}',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 204

    def test_delete_route_404_route_id(self, client):
        response = client.delete(f'{self.CLIENTS_ROUTE_ENDPOINT}/999',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
