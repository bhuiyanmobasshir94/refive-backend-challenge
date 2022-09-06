from rest_framework import serializers

from ..models import *


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = "__all__"
        depth = 0
