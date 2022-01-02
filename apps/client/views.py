from django.db.models import Value
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Handle creating and updating profiles"""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()#todo add account_balance , debit
    filterset_fields = ['first_name', 'last_name', 'national_id', ]
    # permission_classes = (permissions.IsAdminUser)
