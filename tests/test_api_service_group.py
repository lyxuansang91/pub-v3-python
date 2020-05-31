class TestServiceGroupApi():
    ISSUE_KEY = 'IAM-153'
    CLIENTS_SERVICE_GROUP_ENDPOINT = '/api/v1.0/service_groups'

    def test_get_all_service_group_successfully(self, client, service_group_factory):
        service_groups = [service_group_factory.create().to_model(),
                          service_group_factory.create().to_model()]

        response = client.get(f'{self.CLIENTS_SERVICE_GROUP_ENDPOINT}/all',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(service_groups)

        assert data['items'][0]['id'] == service_groups[0]['id']
        assert data['items'][1]['id'] == service_groups[1]['id']
