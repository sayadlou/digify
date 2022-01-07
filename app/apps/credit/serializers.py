from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .policy import TRANSACTION_MAX_DIGITS, TRANSACTION_MIN_VALUE, TRANSACTION_MAX_VALUE
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    """Serializes Account object"""
    branch = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = ('id', 'status', 'owner', 'balance', 'branch')


class AccountUpdateSerializer(serializers.ModelSerializer):
    """Serializes Account object"""

    class Meta:
        model = Account
        fields = ('id', 'status')


class TransactionSerializer(serializers.ModelSerializer):
    """Serializes Transaction object"""

    class Meta:
        model = Transaction
        fields = ('account', 'type', 'source', 'value', 'creat_date_time')
