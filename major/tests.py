from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase,APIClient


class Test_Login_Post(APITestCase):

    def setUp(self):
        self.client =APIClient()
        self.url = reverse('Login')
        User.objects.create_user('Rasul',None,'123456')

    def test_login(self):
        data = {
            'username':'Rasul',
            'password':'123456'
        }
        self.response = self.client.post(self.url,data)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_login_password_post(self):
        data = {
            'username':'Rasul',
            'password':'12345678'
        }
        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_username_post(self):
        data = {
            'username':'Rasula',
            'password':'123456'
        }

        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

