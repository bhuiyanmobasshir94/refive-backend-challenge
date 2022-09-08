from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

User = get_user_model()

# Create your tests here.
class AuthenticationTests(APITestCase):
    def test_autheticattion_success(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], user.id)
        self.assertEqual(response.data["token"], str(user.auth_token))
        user.delete()

    def test_autheticattion_failure(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678910"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        user.delete()

    def test_autheticated_request(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678"},
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])
        response = client.get(reverse("receipt-list-create"))
        self.assertEqual(response.status_code, 200)

        user.delete()

    def test_unautheticated_request(self):
        client = APIClient()
        response = client.get(reverse("receipt-list-create"))
        self.assertEqual(response.status_code, 401)
