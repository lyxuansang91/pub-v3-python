import json

from app.models import OAuth2Client


class TestClientApi():
    ISSUE_KEY = 'IAM-154'
    CLIENTS_API_ENDPOINT = '/api/v1.0/clients'

    def test_create_client_api_should_return_405_when_wrong_method(self, app, client, user):
        response = client.put(TestClientApi.CLIENTS_API_ENDPOINT, headers={
                              'Content-Type': 'application/json'})
        assert response.status_code == 405
        data = response.json
        assert data['message'] == 'The method is not allowed for the requested URL.'

    def test_create_client_return_200_when_create_successfully(self, app, client, user):
        response = client.post(f'{TestClientApi.CLIENTS_API_ENDPOINT}', headers={
            'Content-Type': 'application/json'
        }, data=json.dumps({
            'client_name': 'client name 1',
            'scope': 'openid profile',
            'redirect_uri': 'http://example.com'
        }))

        assert response.status_code == 201
        data = response.json
        assert data['item']['client_id']
        assert data['item']['client_secret']
        assert data['item']['client_name'] == 'client name 1'
        assert data['item']['scope'] == 'openid profile'
        assert data['item']['token_endpoint_auth_method'] == 'client_secret_basic'
        assert data['item']['redirect_uri'] == 'http://example.com'
        oauth_client = OAuth2Client.query.filter_by(
            client_id=data['item']['client_id']).first()
        assert oauth_client.client_id
        assert oauth_client.client_secret
        assert oauth_client.client_name == 'client name 1'
        assert oauth_client.scope == 'openid profile'
        assert oauth_client.redirect_uri == 'http://example.com'

    def test_update_client_should_return_200_when_update_successfully(self, app, client, user, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.put(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}', headers={
            'Content-Type': 'application/json'}, data=json.dumps({'client_id': 'client_id_new'}))
        assert response.status_code == 204
        assert oauth_client.client_id == 'client_id_new'

    def test_update_client_should_return_error(self, app, client, user, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.put(f'{TestClientApi.CLIENTS_API_ENDPOINT}/', headers={
            'Content-Type': 'application/json'}, data=json.dumps({'client_id': 'client_id_new'}))
        assert response.status_code == 404
        data = response.json
        assert data['error']['code'] == 404
        message = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'
        assert data['error']['message'] == message
        response = client.put(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}_error', headers={
            'Content-Type': 'application/json'}, data=json.dumps({'client_id': 'client_id_new'}))
        assert response.status_code == 404
        data = response.json
        assert data['error']['code'] == 404
        assert data['error']['message'] == 'Client ID does not exist'

    def test_delete_client_should_return_success(self, app, client, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.delete(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}', headers={
            'Content-Type': 'application/json'
        })
        assert response.status_code == 204
        _client = OAuth2Client.query.filter_by(
            client_id=oauth_client.client_id).first()
        assert _client is None

    def test_delete_client_should_return_wrong_and_not_remove_client(self, app, client, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.delete(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}_other', headers={
            'Content-Type': 'application/json'
        })
        assert response.status_code == 204
        _client = OAuth2Client.query.filter_by(
            client_id=oauth_client.client_id).first()
        assert _client is not None
        assert _client == oauth_client

    def test_list_clients_should_return_success(self, app, client, user, client_factory):
        oauth_clients = [client_factory.confidential_client(), client_factory.confidential_client()]
        oauth_clients.reverse()
        response = client.get(f'{TestClientApi.CLIENTS_API_ENDPOINT}', headers={
            'Content-Type': 'application/json',
        })

        assert response.status_code == 200
        data = response.json
        assert data['count'] == 2
        assert len(data['items']) == 2

        assert data['items'][0]['client_id'] == oauth_clients[0].client_id
        assert data['items'][1]['client_id'] == oauth_clients[1].client_id

        response = client.get(f'{TestClientApi.CLIENTS_API_ENDPOINT}?sort=client_id_desc&size=1&page=1', headers={
            'Content-Type': 'application/json'
        })

        assert response.status_code == 200
        data = response.json
        assert data['count'] == 2
        assert len(data['items']) == 1
        assert data['items'][0]['client_id'] == oauth_clients[0].client_id

        response = client.get(f'{TestClientApi.CLIENTS_API_ENDPOINT}?sort=client_id_desc&size=1&page=1&filter=client_id', headers={
            'Content-Type': 'application/json'
        })
        assert response.status_code == 200
        data = response.json
        assert data['items'][0].get('client_id') == oauth_clients[0].client_id
        assert data['items'][0].get('client_secret') is None

    def test_get_client_should_return_success(self, app, client, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.get(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}', headers={
            'Content-Type': 'application/json',
        })
        assert response.status_code == 200
        data = response.json
        assert data['item'] == oauth_client.to_model()

    def test_get_client_should_return_error_when_wrong_client_id(self, app, client, client_factory):
        oauth_client = client_factory.confidential_client()
        response = client.get(f'{TestClientApi.CLIENTS_API_ENDPOINT}/{oauth_client.client_id}_other', headers={
            'Content-Type': 'application/json',
        })

        assert response.status_code == 404
        data = response.json
        assert data['error']['code'] == 404
        assert data['error']['message'] == 'Client ID does not exist'
