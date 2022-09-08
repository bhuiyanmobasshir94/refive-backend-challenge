from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .api.serializers import *
from .models import *

User = get_user_model()

# Create your tests here.
class ReceiptTests(APITestCase):
    def test_uploaded_file_extention_support(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678"},
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

        with open(f"{settings.BASE_DIR}/test_files/receipt.txt") as fp:
            response = client.post(reverse("receipt-list-create"), {"receipt": fp})

            self.assertEqual(response.status_code, 201)

        with open(f"{settings.BASE_DIR}/test_files/receipt.pdf", "rb") as fp:
            response = client.post(reverse("receipt-list-create"), {"receipt": fp})

            self.assertEqual(response.status_code, 400)

        user.delete()

    def test_receipt_create_api_response(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678"},
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

        with open(f"{settings.BASE_DIR}/test_files/receipt.txt") as fp:
            response = client.post(reverse("receipt-list-create"), {"receipt": fp})

            self.assertEqual(response.status_code, 201)
            self.assertEqual(type(response.data["blocks"]), list)

        user.delete()

    def test_receipt_list_api_response(self):
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

        receipts = Receipt.objects.all()
        expected_data = ReceiptSerializer(receipts, many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], expected_data)

        user.delete()

    def test_receipt_retrieve_api_response(self):
        user = User.objects.create_user(username="cristian", password="12345678")
        user.save()

        client = APIClient()
        response = client.post(
            reverse("login"),
            {"username": "cristian", "password": "12345678"},
            format="json",
        )
        client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])

        with open(f"{settings.BASE_DIR}/test_files/receipt.txt") as fp:
            response = client.post(reverse("receipt-list-create"), {"receipt": fp})

        receipt = Receipt.objects.first()

        response = client.get(
            reverse("receipt-retrieve-update-delete", args=[receipt.id])
        )

        expected_data = ReceiptSerializer(receipt).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), type(expected_data))

        user.delete()
