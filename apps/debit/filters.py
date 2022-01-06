from django_filters.rest_framework import FilterSet
from .models import Loan


class LoanFilter(FilterSet):
    """Custom Filter for account model"""

    class Meta:
        model = Loan
        fields = {
            'owner': ['exact'],
            'amount': ['gt', 'lt'],

        }
