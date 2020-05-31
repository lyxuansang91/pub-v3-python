class TestSearchServiceResource():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_search_service_resource_successfully(self, client, service_instance, resource_factory):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]
        resources.reverse()
        service_id = service_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/resources',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(resources)

        assert data['items'][0]['id'] == resources[0].id
        assert data['items'][1]['id'] == resources[1].id

    def test_search_service_resource_with_query_normal_successfully(self, client, service_instance, resource_factory):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]
        resources.reverse()
        service_id = service_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/resources?page=1&size=5&sort=code_desc&filter=id name code&is_active=1',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(resources)

        assert data['items'][0]['id'] == resources[0].id
        assert data['items'][1]['id'] == resources[1].id

    def test_search_service_resource_with_query_filter_successfully(self, client, service_instance, resource_factory):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]
        resources.reverse()
        service_id = service_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/resources?name=name&code=code',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(resources)

        assert data['items'][0]['id'] == resources[0].id
        assert data['items'][1]['id'] == resources[1].id

    def test_search_service_resource_with_query_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/resources',
                              headers={'Content-Type': 'application/json'})
        assert response.status_code == 404


class TestGetServiceResourceAll():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_get_service_resource_all_successfully(self, client, service_instance, resource_factory):
        resources = [resource_factory.create(service_instance),
                     resource_factory.create(service_instance)]
        resources.reverse()
        service_id = service_instance.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/resources/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(resources)

        assert data['items'][0]['id'] == resources[0].id
        assert data['items'][1]['id'] == resources[1].id

    def test_get_service_resource_all_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/resources/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 404
