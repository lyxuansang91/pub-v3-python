import json


class TestResourceApi():
    ISSUE_KEY = 'IAM-175'
    CLIENTS_ROLE_ENDPOINT = '/api/v1.0/roles'

    def test_create_role_successfully(self, client, service_instance):
        service_id = service_instance.id

        role_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 201

        data = response.json
        assert data['item']['name'] == role_body['name']
        assert data['item']['code'] == role_body['code']

    def test_create_role_400_role_name_required(self, client, service_instance):
        service_id = service_instance.id

        role_body = {
            'name': '',
            'code': 'code_0',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 400

    def test_create_role_400_role_code_required(self, client, service_instance):
        service_id = service_instance.id

        role_body = {
            'name': 'name_0',
            'code': '',
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 400

    def test_create_role_400_service_id_required(self, client):
        role_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': None
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 400

    def test_create_role_404_service_id(self, client):
        role_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': 999
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 404

    def test_create_role_400_role_code_existed(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        service_id = service_instance.id

        role_body = {
            'name': 'name_0',
            'code': role.code,
            'service_id': service_id
        }
        response = client.post(f'{self.CLIENTS_ROLE_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(role_body))

        assert response.status_code == 400

    def test_update_patch_role_successfully(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        role_id = role.id

        role_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.patch(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(role_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == role_body['name']
        assert data['item']['code'] == role_body['code']

    def test_update_put_role_successfully(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        role_id = role.id

        role_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(role_body))

        assert response.status_code == 200

        data = response.json
        assert data['item']['name'] == role_body['name']
        assert data['item']['code'] == role_body['code']

    def test_update_put_role_404_role_id(self, client):
        role_body = {
            'name': 'name_0',
            'code': 'code_0',
        }
        response = client.put(f'{self.CLIENTS_ROLE_ENDPOINT}/999',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(role_body))

        assert response.status_code == 404

    def test_update_put_role_400_role_code_missing(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        role_id = role.id

        role_body = {
            'name': 'name_0',
            'code': '',
        }
        response = client.put(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(role_body))

        assert response.status_code == 400

    def test_update_put_role_400_role_code_existed(self, client, service_instance, role_factory):
        roles = [role_factory.create(service_instance),
                 role_factory.create(service_instance)]
        role_id = roles[0].id

        role_body = {
            'name': 'name_0',
            'code': roles[1].code,
        }
        response = client.put(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(role_body))

        assert response.status_code == 400

    def test_update_put_role_404_service_id(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        role_id = role.id

        role_body = {
            'name': 'name_0',
            'code': 'code_0',
            'service_id': 999
        }
        response = client.put(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                              headers={'Content-Type': 'application/json'},
                              data=json.dumps(role_body))

        assert response.status_code == 404

    def test_delete_role_successfully(self, client, service_instance, role_factory):
        role = role_factory.create(service_instance)
        role_id = role.id

        response = client.delete(f'{self.CLIENTS_ROLE_ENDPOINT}/{role_id}',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 204

    def test_delete_role_404_role_id(self, client):
        response = client.delete(f'{self.CLIENTS_ROLE_ENDPOINT}/999',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
