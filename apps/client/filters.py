from django_filters.rest_framework import FilterSet
from .models import Client


class ClientFilter(FilterSet):
    """Custom Filter for client model"""
    class Meta:
        model = Client
        fields = {
            'first_name': ['exact'],
            'last_name': ['exact'],
            'national_id': ['exact'],
            'balance': ['gt', 'lt'],
            'total_loan': ['gt', 'lt'],
            'total_debit': ['gt', 'lt'],
        }
