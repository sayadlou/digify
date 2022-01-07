from django_filters.rest_framework import FilterSet
from .models import Account, Transaction


class AccountFilter(FilterSet):
    """Custom Filter for account model"""

    class Meta:
        model = Account
        fields = {
            'owner': ['exact'],
            'balance': ['gt', 'lt'],

        }


class TransactionFilter(FilterSet):
    """Custom Filter for Transaction model"""

    class Meta:
        model = Transaction
        fields = {
            'account': ['exact'],
            'type': ['exact'],
            'source': ['exact'],
            'value': ['gt', 'lt'],

        }
