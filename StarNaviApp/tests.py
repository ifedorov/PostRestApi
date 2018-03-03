import json

from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
# Create your tests here.
from StarNaviApp.models import Post


class SimpleTest(TestCase):
    fixtures = ['test-data.json']
    def setUp(self):

        token = Token.objects.get(user__email='dont@mail.me')

        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.token = token.key
        self.post_id = Post.objects.all().first().id


    def test_token(self):

        response = self.api_client.post('/v1/user/token', data={'email': 'dont@mail.me', 'password': 'aNe9Q!ih#*'})
        data = json.loads(response.content)
        self.assertEqual(data['token'], self.token)


    def test_post_create(self):
        text = "text"
        response = self.api_client.post('/v1/post', data={'content': '\n'.join(text)})
        self.assertEqual(response.status_code, 201)


    def test_post_like(self):
        response = self.api_client.put('/v1/post/{0}/like'.format(self.post_id))
        self.assertEqual(response.status_code, 201)


    def test_post_unlike(self):
        response = self.api_client.put('/v1/post/{0}/unlike'.format(self.post_id))
        self.assertEqual(response.status_code, 201)