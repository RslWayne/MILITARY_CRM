from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase,APIClient
from .models import *
import json


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


class TestDossierMethods(APITestCase):
    def setUp(self):
        self.url = reverse('dossier')
        self.client = APIClient()
        self.user = User.objects.create_user(username='maksim', password='123456')
        self.dossier = Dossier.objects.create(user=self.user, full_name='maksim', date_birth='2021-05-09',
                                              gender='M',
                                              )


    def test_dossier_put_ok(self):
        self.client.login(username='maksim', password='123456')
        data = {
            "id": 23,
            "full_name": "maks312312312",
            "date_birth": "1998-07-26",
            "gender": "M",
            "cars": [
            {
                "car_id": 1,
                "mark": "toyota camry",
                "year":"2000-03-03",
                "number":"22",
                "color":"red",
                "type":"sport"
            },
        ],
            "schools": [
            {
                "id": 1,
                "school_name": "KSTU",
                "end_date": "2021-02-20",
                "major": "BA"
            }
            ],
            "war_crafts": [
                {
                    "id": 1,
                    "military_area": "sofa warrior",
                    "end_date": "2021-02-20",
                    "major": "BA"
                }
            ],
        }

        self.response = self.client.put(self.url, data=data,format='json')
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.client.login(username='maksim', password='123456')
        self.response = self.client.delete(self.url)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


