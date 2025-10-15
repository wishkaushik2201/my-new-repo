import pytest
from django.urls import reverse
from rest_framework.test import APITestCase
from api.models import User
from django.contrib.auth.hashers import make_password

class UserAuthTests(APITestCase):

    def test_user_login(self):
        # Create user
        user = User.objects.create(
            email="sharma.vishal.2201@gmail.com",
            username="vishal",
            password=make_password("Vs42653@")
        )

        url = reverse('user-login')  # DRF router basename 'user' + action 'login'
        data = {"email": user.email, "password": "Vs42653@"}

        response = self.client.post(url, data, format='json')
        # debug print (optional)
        print(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Login successful")
        self.assertEqual(response.data['user']['email'], user.email)
