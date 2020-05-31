import json


class TestDashboardApi():
    ISSUE_KEY = 'IAM-167'
    API_ENDPOINT = '/api/v1.0/dashboard'

    def test_get_admin_activeness(self, client, service_instance):
        response = client.get(f'{self.API_ENDPOINT}/admin/activeness',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200
