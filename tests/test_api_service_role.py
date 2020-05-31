class TestSearchServiceRole():
    ISSUE_KEY = 'IAM-175'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_search_service_role_successfully(self, client, service_instance, role_factory):
        roles = [role_factory.create(service_instance).to_model(),
                 role_factory.create(service_instance).to_model()]
        roles.reverse()
        service = service_instance.to_model()
        service_id = service['id']

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/roles',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(roles)

        assert data['items'][0]['id'] == roles[0]['id']
        assert data['items'][1]['id'] == roles[1]['id']

    def test_search_service_role_with_query_normal_successfully(self, client, service_instance, role_factory):
        roles = [role_factory.create(service_instance).to_model(),
                 role_factory.create(service_instance).to_model()]
        roles.reverse()
        service = service_instance.to_model()
        service_id = service['id']

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/roles?page=1&size=5&sort=code_desc&filter=id name code',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(roles)

        assert data['items'][0]['id'] == roles[0]['id']
        assert data['items'][1]['id'] == roles[1]['id']

    def test_search_service_role_with_query_filter_successfully(self, client, service_instance, role_factory):
        roles = [role_factory.create(service_instance).to_model(),
                 role_factory.create(service_instance).to_model()]
        roles.reverse()
        service = service_instance.to_model()
        service_id = service['id']

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/roles?name=name&code=code',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(roles)

        assert data['items'][0]['id'] == roles[0]['id']
        assert data['items'][1]['id'] == roles[1]['id']

    def test_search_service_role_with_query_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/roles',
                              headers={'Content-Type': 'application/json'})
        assert response.status_code == 404


class TestGetServiceRoleAll():
    ISSUE_KEY = 'IAM-175'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_get_service_role_all_successfully(self, client, service_instance, role_factory):
        roles = [role_factory.create(service_instance).to_model(),
                 role_factory.create(service_instance).to_model()]
        roles.reverse()
        service = service_instance.to_model()
        service_id = service['id']

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/roles/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(roles)

        assert data['items'][0]['id'] == roles[0]['id']
        assert data['items'][1]['id'] == roles[1]['id']

    def test_get_service_role_all_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/roles/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
