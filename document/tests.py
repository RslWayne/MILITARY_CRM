from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase,APIClient
from .models import Document
from .factory import populate_test_db_docs,populate_test_db_

# Create your tests here.


class TestDocumentRulesGet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        # create user and group
        populate_test_db_(User,Group)
        # create docs for users
        populate_test_db_docs(Document)

    def test_serjant_permissions(self):
        self.client.login(username='serjant',password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response,text='private document',status_code=200)

    def test_serjant_no_permissions(self):
        self.client.login(username='serjant',password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertNotContains(self.response,text='secret document',status_code=200)

    def test_document_create(self):
        self.client.login(username='general',password='123456')
        data = {
            'title':'asdasd',
            'status':'active',
            'text':'1223',
            'date_expired':'2020-06-06',
            'document_root':'public'
        }
        self.response = self.client.post(self.url,data)
        print(self.response.json())
        self.assertEqual(self.response.status_code,status.HTTP_201_CREATED)


class TestPost(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        populate_test_db_(User, Group)
        populate_test_db_docs(Document)

    def test_document_serjant(self):
        self.client.login(username='serjant', password='123456')
        data = {
            'title': 'asdasd',
            'status': 'active',
            'text': '1223',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertNotEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_document_president(self):
        self.client.login(username='president', password='123456')
        data = {
            'title': 'asdasd',
            'status': 'active',
            'text': '1223',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_document_no_president(self):
        self.client.login(username='president', password='123456')
        data = {
            'title': 'asdasd',
            'status': 'active',
            'text': '1223',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        print(self.response.json())
        self.assertNotEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


    def test_general_create_error(self):
        self.client.login(username = 'general' , password = '123456')
        data = {
            'title': 'assdaddasd',
            'status': 'active',
            'text': '1233',
            'date_expired':'2020-06-06',
            'document_root':'top-secret'
        }
        self.response = self.client.post(self.url,data)
        print(self.response.json())
        self.assertContains(self.response,text='You have no permissions!',status_code = 400)

    def test_president_create(self):
        self.client.login(username='president',password = '123456')
        data = {
            'title': 'assdaddasd',
            'status': 'active',
            'text': '1233',
            'date_expired': '2020-06-06',
            'document_root': 'top-secret'
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class TestDateExpiredDocument(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # doc.id = 1
        self.doc1 = Document.objects.create(title='not expired doc',
                                date_expired = "2021-12-31",document_root = 'private')
        # doc.id = 2
        self.doc2 = Document.objects.create(title='expired doc',
                                date_expired = "2021-05-09",document_root='private',status='dead')
        populate_test_db_(User,Group)

    def test_get_not_expired(self):
        self.url = reverse('documents-detail',kwargs={'pk':self.doc1.id})
        self.client.login(username='general',password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response,'active',status_code=200)

    def test_get_expired(self):
        self.url = reverse('documents-detail', kwargs={'pk': self.doc2.id})
        self.client.login(username='general', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response, 'Страница не найдена.', status_code=404)



