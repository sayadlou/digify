from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class AccountTests(APITestCase):
    modir_token = 0
    shobe1_token = 0
    shobe2_token = 0

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser(
            username='modir',
            email='bank@meli.com',
            password='ASeeRGH5562..'
        )
        cls.modir_token = Token.objects.create(user=user)
        user = User.objects.create_user(
            username='shobe1',
            email='shobe1@meli.com',
            password='ASeeRGH5562..'
        )
        cls.shobe1_token = Token.objects.create(user=user)
        user = User.objects.create_user(
            username='shobe2',
            email='shobe2@meli.com',
            password='ASeeRGH5562..'
        )
        cls.shobe2_token = Token.objects.create(user=user)

    def test_credit_url_access(self):
        """
        Ensure  credit url is authenticated
        """
        client = APIClient()
        url = '/apiv1/account/'
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.modir_token}')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.shobe1_token}')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_create(self):
        """"
            check account creation
        """
        client = APIClient(enforce_csrf_checks=False)
        url = '/apiv1/client/'
        data = {
            "first_name": "saeid",
            "last_name": "sayadlou",
            "national_id": "0084017449",
            "mobile_number": "09132346829",
            "balance": '100000',
            "total_loan": '0',
            "total_debit": '0'
        }
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.shobe1_token}')
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = '/apiv1/account/'
        data = {
            "status": "Open",
            "balance": "10000",
            "owner": response.data['id'],

        }
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.shobe1_token}')
        response = client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/apiv1/transaction/'
        data = {
            "account": response.data['id'],
            "type": "Deposit",
            "value": "1500",

        }
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.shobe1_token}')
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

