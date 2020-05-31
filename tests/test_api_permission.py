import json


class TestResourceApi():
    ISSUE_KEY = 'IAM-108'
    CLIENTS_PERMISSION_ENDPOINT = '/api/v1.0/permissions'

    def test_create_permission_successfully(self, client, resource_instance, action_instance):
        resource_id = resource_instance.id
        action_id = action_instance.id

        permission_body = {
            'name': 'name_0',
            'code': f'{resource_instance.code}:{action_instance.code}',
            'resource_id': resource_id,
            'action_id': action_id,
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 201

        data = response.json
        assert data['item']['code'] == '{}:{}'.format(resource_instance.code, action_instance.code)

    def test_create_permission_400_permission_action_required(self, client):
        permission_body = {
            'service_id': 1
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 400

    def test_create_permission_400_permission_resource_required(self, client):
        permission_body = {
            'action_id': 1
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 400

    def test_create_permission_404_resource_id(self, client, action_instance):
        action_id = action_instance.id

        permission_body = {
            'resource_id': 999,
            'action_id': action_id
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 404

    def test_create_permission_404_action_id(self, client, resource_instance):
        resource_id = resource_instance.id

        permission_body = {
            'resource_id': resource_id,
            'action_id': 999
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 404

    def test_create_permission_400_permission_existed(self, client, permission_factory, resource_instance, action_instance):
        permission_factory.create(resource_instance, action_instance)
        resource_id = resource_instance.id
        action_id = action_instance.id

        permission_body = {
            'resource_id': resource_id,
            'action_id': action_id
        }
        response = client.post(f'{self.CLIENTS_PERMISSION_ENDPOINT}',
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps(permission_body))

        assert response.status_code == 400

    def test_delete_permission_successfully(self, client, permission_factory, resource_instance, action_instance):
        permission = permission_factory.create(resource_instance, action_instance)
        permission_id = permission.id

        response = client.delete(f'{self.CLIENTS_PERMISSION_ENDPOINT}/{permission_id}',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 204

    def test_delete_permission_404_permission_id(self, client):
        response = client.delete(f'{self.CLIENTS_PERMISSION_ENDPOINT}/999',
                                 headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
