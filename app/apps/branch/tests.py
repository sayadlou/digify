from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
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

    def test_branch_url_access(self):
        """
        Ensure just admin has access to branch url
        """
        response = self.client.get('/apiv1/branch/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.modir_token}')
        response = self.client.get('/apiv1/branch/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.shobe1_token}')
        response = self.client.get('/apiv1/branch/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
