from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """Serializes Account object"""

    class Meta:
        model = Loan
        fields = ('id', 'owner', 'amount', 'total_installment', 'amount', )
