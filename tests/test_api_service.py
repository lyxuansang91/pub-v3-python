import json


class TestServiceApi():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_search_service_successfully(self, client, service_group_instance, service_factory):
        services = [service_factory.create(service_group=service_group_instance),
                    service_factory.create(service_group=service_group_instance)]
        services.reverse()

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(services)

        assert data['items'][0]['id'] == services[0].id
        assert data['items'][1]['id'] == services[1].id

    def test_search_service_with_query_normal_successfully(self, client, service_group_instance, service_factory):
        services = [service_factory.create(service_group=service_group_instance),
                    service_factory.create(service_group=service_group_instance)]
        services.reverse()

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}?page=1&size=5&sort=code_desc&filter=id name code&is_active=1',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(services)

        assert data['items'][0]['id'] == services[0].id
        assert data['items'][1]['id'] == services[1].id

    def test_search_service_with_query_filter_successfully(self, client, service_group_instance, service_factory):
        services = [service_factory.create(service_group=service_group_instance),
                    service_factory.create(service_group=service_group_instance)]
        services.reverse()
        service_group_id = service_group_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}?name=name&code=code&service_group_id={service_group_id}',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(services)

        assert data['items'][0]['id'] == services[0].id
        assert data['items'][1]['id'] == services[1].id

    def test_search_service_with_query_404_service_group_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}?service_group_id=999',
                              headers={'Content-Type': 'application/json'})
        assert response.status_code == 404


class TestGetService():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_get_service_successfully(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group=service_group_instance)
        service_id = service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert data['item']['id'] == service.id
        assert data['item']['name'] == service.name
        assert data['item']['code'] == service.code

    def test_get_service_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 404


class TestCreateService():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_create_service_successfully(self, client, service_group_instance):
        service_group_id = service_group_instance.id

        service_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_group_id': service_group_id,
            'public_url': 'http://example.com',
            'private_url': 'http://example.com'
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 201

        data = response.json
        assert data['item']['name'] == service_body['name']
        assert data['item']['code'] == service_body['code']

    def test_create_service_400_service_name_required(self, client, service_group_instance):
        service_group_id = service_group_instance.id

        service_body = {
            'name': '',
            'code': 'code_0',
            'service_group_id': service_group_id
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 400

    def test_create_service_400_service_code_required(self, client, service_group_instance):
        service_group_id = service_group_instance.id

        service_body = {
            'name': 'name_0',
            'code': '',
            'service_group_id': service_group_id
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 400

    def test_create_service_400_service_group_required(self, client):
        service_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_group_id': 0
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 400

    def test_create_service_404_service_group_id(self, client):
        service_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_group_id': 999
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 404

    def test_create_service_400_service_code(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_group_id = service_group_instance.id

        service_body = {
            'name': 'name_0',
            'code': service.code,
            'service_group_id': service_group_id
        }
        response = client.post(f'{self.CLIENTS_SERVICE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(service_body))

        assert response.status_code == 400


class TestUpdateService():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_update_patch_service_successfully(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        service_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.patch(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(service_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == service_body['name']
        assert data['item']['code'] == service_body['code']

    def test_update_put_service_successfully(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        service_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(service_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == service_body['name']
        assert data['item']['code'] == service_body['code']

    def test_update_put_service_404_service_id(self, client):
        service_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_SERVICE_ENDPOINT}/999',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(service_body))

        assert response.status_code == 404

    def test_update_put_service_400_service_code_missing(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        service_body = {
            'name': 'name_0',
            'code': '',
        }
        response = client.put(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(service_body))

        assert response.status_code == 400

    def test_update_put_service_400_service_code_existed(self, client, service_group_instance, service_factory):
        services = [service_factory.create(service_group_instance),
                    service_factory.create(service_group_instance)]
        service_id = services[0].id

        service_body = {
            'name': 'name_0',
            'code': services[1].code,
        }
        response = client.put(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(service_body))

        assert response.status_code == 400

    def test_update_put_service_404_service_group_id(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        service_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_group_id': 999
        }
        response = client.put(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(service_body))

        assert response.status_code == 404


class TestDeleteService():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_delete_service_successfully(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        response = client.delete(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 204

    def test_delete_service_404_service_id(self, client):
        response = client.delete(f'{self.CLIENTS_SERVICE_ENDPOINT}/999',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 404


class TestGetServiceReference():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_get_service_reference_successfully(self, client, service_group_instance, service_factory):
        service = service_factory.create(service_group_instance)
        service_id = service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/reference',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert data['item'] == {
            'user': 0, 'scope': 0, 'role': 0, 'resource': 0, 'route': 0, 'permission': 0
        }

    def test_get_service_reference_404_service_id(self, client):

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/reference',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
