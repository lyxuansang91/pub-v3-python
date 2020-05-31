import json
from random import randrange

from app.extensions import db

from .factories import UserFactory

DEFAULT_COUNT = 500


class TestBaseOnApiUser:
    ISSUE_KEY = 'IAM-162'
    ENDPOINT = '/api/v1.0/users/'

    def test_able_to_get_one_user(self, client, user):
        res = client.get(self.ENDPOINT + user.id)
        assert res.status_code == 200
        res = res.json
        item = res.get('item')
        assert item
        assert item.get('id')
        assert item.get('name')
        assert item.get('email')
        assert item.get('phone_number')

    def test_get_not_found_user(self, client):
        res = client.get(self.ENDPOINT + 'invalid-user-id')
        assert res.status_code == 404

    def test_update_user_using_put(self, client, user):
        res = client.put(self.ENDPOINT + user.id,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps({
                             'name': '_New Name_',
                             'avatar_url': 'Handsome avatar url'
                         }))
        assert res.status_code == 200
        assert res.json.get('item').get('avatar_url')

        res = client.put(self.ENDPOINT + user.id,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps({
                             'name': 'New Name',
                         }))
        assert res.status_code == 200
        item = res.json.get('item')
        assert item.get('name') == 'New Name'
        assert not item.get('avatar_url')

    def test_update_user_using_patch(self, client, user):
        res = client.patch(self.ENDPOINT + user.id,
                           headers={'Content-Type': 'application/json'},
                           data=json.dumps(
                               {'avatar_url': 'Handsome avatar url'}))
        assert res.status_code == 200
        item = res.json.get('item')
        assert item.get('name') == user.name
        assert item.get('avatar_url')

    def test_input_invalid_info_when_update_user(self, client, user):
        res = client.put(self.ENDPOINT + user.id,
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps({}))
        assert res.status_code == 400
        message = res.json.get('error').get('message')
        assert message.get('name')

    def test_able_to_delete_user(self, client, user):
        res = client.delete(self.ENDPOINT + user.id)
        assert res.status_code == 204
        assert not res.data
        res = client.get(self.ENDPOINT + user.id)
        assert res.status_code == 404


class TestBaseListOnApiUser:
    ISSUE_KEY = 'IAM-162'
    ENDPOINT = '/api/v1.0/users'

    def _init_users(self, count=DEFAULT_COUNT):
        for i in range(count):
            user = UserFactory()
            db.session.add(user)
        db.session.commit()

    def _check_error_message(self, res, message):
        assert res.json.get('error').get('message') == message
        return True

    def test_able_to_get_success_response(self, app, client):
        self._init_users()
        res = client.get(self.ENDPOINT)
        assert res.status_code == 200
        res = res.json
        items = res.get('items')
        count = res.get('count')
        page = res.get('page')
        size = res.get('size')
        assert len(items) == app.config.get('API_ITEMS_MAX_SIZE') == size
        assert count == DEFAULT_COUNT
        assert page == 1

    def test_invalid_input_schema(self, client):
        self._init_users()
        res = client.get(self.ENDPOINT,
                         query_string={
                             'page': 'string',
                             'size': 'string',
                             'birthday': 'string',
                         })
        assert res.status_code == 400
        message = res.json.get('error').get('message')
        assert 'page' in message.keys()
        assert 'size' in message.keys()
        assert 'birthday' in message.keys()

    def test_invalid_sort(self, client):
        self._init_users()
        res = client.get(self.ENDPOINT, query_string={'sort': 'invalid_sort'})
        assert res.status_code == 400
        assert self._check_error_message(res, '`sort` is not valid')

    def test_invalid_filter(self, client):
        self._init_users()
        res = client.get(
            self.ENDPOINT,
            query_string={'filter': 'field_not_correct another_field'})
        assert res.status_code == 400
        assert self._check_error_message(res, '`filter` is not valid')

    def test_able_to_limit_data_size(self, app, client):
        self._init_users()
        qsize = randrange(1, app.config.get('API_ITEMS_MAX_SIZE'))
        res = client.get(self.ENDPOINT, query_string={'size': qsize})
        assert res.status_code == 200
        size = res.json.get('size')
        assert size == qsize == len(res.json.get('items'))

    def test_not_able_to_query_limit_data_over_max(self, app, client):
        self._init_users()
        qsize = int(1E5)
        res = client.get(self.ENDPOINT, query_string={'size': qsize})
        assert res.status_code == 200
        size = res.json.get('size')
        assert size == app.config.get('API_ITEMS_MAX_SIZE')

    def test_able_to_paging_data(self, app, client):
        self._init_users()
        qsize = randrange(1, app.config.get('API_ITEMS_MAX_SIZE'))
        divided = 1 if DEFAULT_COUNT % qsize == 0 else 0
        last_page = DEFAULT_COUNT // qsize + divided
        res = client.get(self.ENDPOINT,
                         query_string={
                             'size': qsize,
                             'page': last_page
                         })
        assert res.status_code == 200
        print('res:', res.json)
        assert len(res.json.get(
            'items')) == DEFAULT_COUNT % qsize if divided else qsize

    def test_able_to_filter_data(self, client):
        self._init_users()
        res = client.get(self.ENDPOINT,
                         query_string={
                             'size': 20,
                             'filter': 'id name email'
                         })
        assert res.status_code == 200
        items = res.json.get('items')
        for item in items:
            assert set(['id', 'name', 'email']) == set(item.keys())

    def test_able_to_sort_data(self, client):
        self._init_users()
        res = client.get(self.ENDPOINT, query_string={'sort': 'id_desc'})
        assert res.status_code == 200
        items = res.json.get('items')
        for i in range(len(items) - 1):
            assert items[i]['id'] >= items[i + 1]['id']

    def test_able_to_search_data(self, client):
        self._init_users()
        res = client.get(self.ENDPOINT, query_string={'name': '27'})
        assert res.status_code == 200
        items = res.json.get('items')
        for item in items:
            assert '27' in item.get('name')

    def test_able_to_create_new_user(self, client):
        res = client.post(self.ENDPOINT,
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps({
                              'name': 'User',
                              'phone_number': '0123456789'
                          }))
        assert res.status_code == 201
        item = res.json.get('item')
        assert item.get('id')
        assert item.get('name') == 'User'
        assert item.get('phone_number') == '0123456789'

    def test_should_error_when_input_invalid_data(self, client):
        res = client.post(self.ENDPOINT,
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps({
                              'birthday': 'invalid-birthday',
                              'injection': 'danger-value'
                          }))
        assert res.status_code == 400
        message = res.json.get('error').get('message')
        assert message.get('name')
        assert message.get('birthday')
        assert message.get('injection')

    def test_should_error_for_create_duplicate_keys(self, client, user):
        res = client.post(self.ENDPOINT,
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps({
                              'name': 'User',
                              'email': user.email
                          }))
        assert res.status_code == 400
        assert res.json.get('error').get('message')
