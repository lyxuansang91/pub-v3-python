class TestSearchServicePermission():
    ISSUE_KEY = 'IAM-108'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_search_service_permission_successfully(self, client, resource_instance, action_instance, permission_factory):
        permissions = [permission_factory.create(resource_instance, action_instance),
                       permission_factory.create(resource_instance, action_instance)]
        permissions.reverse()
        service_id = resource_instance.service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/permissions',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(permissions)

        assert data['items'][0]['id'] == permissions[0].id
        assert data['items'][1]['id'] == permissions[1].id

    def test_search_service_permission_with_query_normal_successfully(self, client, resource_instance, action_instance, permission_factory):
        permissions = [permission_factory.create(resource_instance, action_instance),
                       permission_factory.create(resource_instance, action_instance)]
        permissions.reverse()
        service_id = resource_instance.service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/permissions?page=1&size=5&sort=code_desc&filter=id name code',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(permissions)

        assert data['items'][0]['id'] == permissions[0].id
        assert data['items'][1]['id'] == permissions[1].id

    def test_search_service_permission_with_query_filter_successfully(self, client, resource_instance, action_instance, permission_factory):
        permissions = [permission_factory.create(resource_instance, action_instance),
                       permission_factory.create(resource_instance, action_instance)]
        permissions.reverse()
        service_id = resource_instance.service.id
        resource_id = resource_instance.id
        action_id = action_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/permissions?name=name&code=code&resource_id={resource_id}&action_id={action_id}',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(permissions)

        assert data['items'][0]['id'] == permissions[0].id
        assert data['items'][1]['id'] == permissions[1].id

    def test_search_service_permission_with_query_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/permissions',
                              headers={'Content-Type': 'application/json'})
        assert response.status_code == 404


class TestGetServicePermissionAll():
    ISSUE_KEY = 'IAM-108'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_get_service_permission_all_successfully(self, client, resource_instance, action_instance, permission_factory):
        permissions = [permission_factory.create(resource_instance, action_instance),
                       permission_factory.create(resource_instance, action_instance)]
        permissions.reverse()
        service_id = resource_instance.service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/permissions/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(permissions)

        assert data['items'][0]['id'] == permissions[0].id
        assert data['items'][1]['id'] == permissions[1].id

    def test_get_service_permission_all_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/permissions/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
