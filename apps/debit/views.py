from django.db import transaction
from django.shortcuts import render
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.viewsets import GenericViewSet

from .filters import LoanFilter
from .models import Loan
from .serializers import LoanSerializer


class LoanViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Handle creating and listing Account of clients"""
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    filterset_class = LoanFilter
    permission_classes = (permissions.IsAuthenticated,)



