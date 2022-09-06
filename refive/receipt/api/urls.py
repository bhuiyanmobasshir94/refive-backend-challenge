from django.urls import path

from .views import *

urlpatterns = [
    path("", ReceiptListCreateAPIView.as_view()),
    path("<uuid:pk>/", ReceiptRetrieveUpdateDestroyAPIView.as_view()),
]
