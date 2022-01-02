from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializes Client object"""

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'national_id', 'is_new')
