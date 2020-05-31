class TestSearchServicePermission():
    ISSUE_KEY = 'IAM-108'
    CLIENTS_SERVICE_ENDPOINT = '/api/v1.0/services'

    def test_search_service_route_successfully(self, client, resource_instance, action_instance, permission_factory, route_factory):
        permission = permission_factory.create(resource_instance, action_instance)
        routes = [route_factory.create(permission, resource_instance),
                  route_factory.create(permission, resource_instance)]
        routes.reverse()
        service_id = resource_instance.service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/routes',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(routes)

        assert data['items'][0]['id'] == routes[0].id
        assert data['items'][1]['id'] == routes[1].id

    def test_search_service_route_with_query_normal_successfully(self, client, resource_instance, action_instance, permission_factory, route_factory):
        permission = permission_factory.create(resource_instance, action_instance)
        routes = [route_factory.create(permission, resource_instance),
                  route_factory.create(permission, resource_instance)]
        routes.reverse()
        service_id = resource_instance.service.id

        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/routes?page=1&size=5&sort=name_desc&filter=id name',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(routes)

        assert data['items'][0]['id'] == routes[0].id
        assert data['items'][1]['id'] == routes[1].id

    def test_search_service_route_with_query_filter_successfully(self, client, resource_instance, action_instance, permission_factory, route_factory):
        permission = permission_factory.create(resource_instance, action_instance)
        routes = [route_factory.create(permission, resource_instance),
                  route_factory.create(permission, resource_instance)]
        routes.reverse()
        service_id = resource_instance.service.id
        permission_id = permission.id
        resource_id = resource_instance.id

        query = f'?name=name&reg_uri=reg_uri&method=GET&resource_id={resource_id}&required_permission_id={permission_id}'
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/{service_id}/routes{query}',
                              headers={'Content-Type': 'application/json'})

        assert response.status_code == 200

        data = response.json
        assert len(data['items']) == len(routes)

        assert data['items'][0]['id'] == routes[0].id
        assert data['items'][1]['id'] == routes[1].id

    def test_search_service_route_with_query_404_service_id(self, client):
        response = client.get(f'{self.CLIENTS_SERVICE_ENDPOINT}/999/routes',
                              headers={'Content-Type': 'application/json'})
        assert response.status_code == 404
