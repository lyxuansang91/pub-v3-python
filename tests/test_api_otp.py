# -*- coding: utf-8 -*-
from time import sleep
from app.utils.crypto import generate_opt_code


class TestAPIOTP:

    ISSUE_KEY = 'IAM-180'
    PREFIX_ENDPOINT = '/api/v1.0/otp'

    def test_api_should_return_415_if_media_type_is_unsupported(self, client, user):
        endpoints = (self.PREFIX_ENDPOINT + '/generate',
                     self.PREFIX_ENDPOINT + '/validate')
        for endpoint in endpoints:
            response = client.post(endpoint, data={'email': user.email})
            assert response.status_code == 415

    def test_api_should_return_400_if_user_does_not_exist(self, client):
        endpoints = (self.PREFIX_ENDPOINT + '/generate',
                     self.PREFIX_ENDPOINT + '/validate')
        for endpoint in endpoints:
            response = client.post(endpoint, json={'email': 'test@teko.vn'})
            assert response.status_code == 400
            response = client.post(endpoint, json={'phone_number': '0123-456-789'})
            assert response.status_code == 400

    def test_otp_generator_api(self, client, user):
        response = client.post('/api/v1.0/otp/generate', json={'email': user.email})
        assert response.status_code == 200
        assert user.otp_key is not None

    def test_otp_validator_api(self, client, user):
        response = client.post('/api/v1.0/otp/generate', json={'email': user.email})
        assert response.status_code == 200
        otp = generate_opt_code(otp_enckey=user.otp_key)
        response = client.post('/api/v1.0/otp/validate', json={'email': user.email, 'otp_code': otp.token})
        assert response.status_code == 200
        assert response.json['is_valid'] is True
        response = client.post('/api/v1.0/otp/validate', json={'email': user.email, 'otp_code': otp.token})
        assert response.status_code == 200
        assert response.json['is_valid'] is False
        otp = generate_opt_code(otp_enckey=user.otp_key)
        sleep(3)
        response = client.post('/api/v1.0/otp/validate', json={'email': user.email, 'otp_code': otp.token})
        assert response.status_code == 200
        assert response.json['is_valid'] is False
