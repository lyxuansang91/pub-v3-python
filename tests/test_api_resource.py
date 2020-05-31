import json


class TestResourceApi():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_RESOURCE_ENDPOINT = '/api/v1.0/resources'

    def test_create_resource_successfully(self, client, service_instance):
        service_id = service_instance.id

        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 201

        data = response.json
        assert data['item']['name'] == resource_body['name']
        assert data['item']['code'] == resource_body['code']

    def test_create_resource_400_resource_name_required(self, client, service_instance):
        service_id = service_instance.id

        resource_body = {
            'name': '',
            'code': 'code_0',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_create_resource_400_resource_code_required(self, client, service_instance):
        service_id = service_instance.id

        resource_body = {
            'name': 'name_0',
            'code': '',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_create_resource_400_service_id_required(self, client):
        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': None
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_create_resource_404_service_id(self, client):
        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': 999
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 404

    def test_create_resource_400_resource_code_existed(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        service_id = service_instance.id

        resource_body = {
            'name': 'name_0',
            'code': resource.code,
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_RESOURCE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_update_patch_resource_successfully(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        resource_id = resource.id

        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.patch(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(resource_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == resource_body['name']
        assert data['item']['code'] == resource_body['code']

    def test_update_put_resource_successfully(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        resource_id = resource.id

        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(resource_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == resource_body['name']
        assert data['item']['code'] == resource_body['code']

    def test_update_put_resource_404_resource_id(self, client):
        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_RESOURCE_ENDPOINT}/999',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(resource_body))

        assert response.status_code == 404

    def test_update_put_resource_400_resource_code_missing(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        resource_id = resource.id

        resource_body = {
            'name': 'name_0',
            'code': '',
        }
        response = client.put(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_update_put_resource_400_resource_code_existed(self, client, service_instance, resource_factory):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]
        resource_id = resources[0].id

        resource_body = {
            'name': 'name_0',
            'code': resources[1].code,
        }
        response = client.put(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(resource_body))

        assert response.status_code == 400

    def test_update_put_resource_404_service_id(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        resource_id = resource.id

        resource_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': 999
        }
        response = client.put(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(resource_body))

        assert response.status_code == 404

    def test_delete_resource_successfully(self, client, service_instance, resource_factory):
        resource = resource_factory.create(service_instance)
        resource_id = resource.id

        response = client.delete(f'{self.CLIENTS_RESOURCE_ENDPOINT}/{resource_id}',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 204

    def test_delete_resource_404_resource_id(self, client):
        response = client.delete(f'{self.CLIENTS_RESOURCE_ENDPOINT}/999',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
