from django.urls import path

from .views import *

urlpatterns = [
    path("", ReceiptListCreateAPIView.as_view(), name="receipt-list-create"),
    path("<uuid:pk>/", ReceiptRetrieveUpdateDestroyAPIView.as_view(), name="receipt-retrieve-update-delete"),
]
