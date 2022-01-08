from decimal import Decimal

from django.db import transaction
from django.http import QueryDict
from django.shortcuts import render
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from .filters import LoanFilter
from .models import Loan
from .serializers import LoanSerializer
from ..client.models import Client


class LoanViewSet(mixins.ListModelMixin,
                  GenericViewSet):
    """Handle creating and listing Account of clients"""
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    filterset_class = LoanFilter
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            print(request.data['owner'])
            account = Client.objects.select_for_update().get(pk=request.data['owner'])
            account.total_loan += Decimal(request.data['amount'])
            account.total_debit += Decimal(request.data['remained_amount'])
            self.perform_create(serializer)
            account.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
