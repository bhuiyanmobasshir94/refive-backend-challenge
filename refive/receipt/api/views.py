from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from ..models import *
from ..services import *
from .serializers import *


class ReceiptListCreateAPIView(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["receipt__name"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.save()
        blocks = get_coords(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(blocks, status=status.HTTP_201_CREATED, headers=headers)


class ReceiptRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ["receipt__name"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
