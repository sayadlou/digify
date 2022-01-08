from rest_framework import serializers

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """Serializes Account object"""
    branch = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Loan
        fields = (
            'id', 'owner', 'amount', 'total_installment', 'amount', 'remained_amount', 'remained_installment', 'branch')
