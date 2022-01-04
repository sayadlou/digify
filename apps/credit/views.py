from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .Policy import ACCOUNT_MIN_BALANCE, ACCOUNT_MAX_BALANCE
from .filters import AccountFilter, TransactionFilter
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from ..client.models import Client


class AccountViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """Handle creating and listing Account of clients"""
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    filterset_class = AccountFilter
    permission_classes = (permissions.IsAuthenticated,)


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """Handle creating and listing Transaction of clients"""
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilter
    permission_classes = (permissions.IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__()
        self.headers = None
        self.serializer = None

    def validate_transfer(self, account_balance, source_balance, action_value):
        if account_balance + int(action_value) > ACCOUNT_MAX_BALANCE:
            raise ValidationError("value of transaction in not valid")
        if source_balance - int(action_value) < ACCOUNT_MIN_BALANCE:
            raise ValidationError("value of transaction in not valid")

    def validate_desposit_and_withdrawal(self, account_balance, action_value, action_type):
        if action_type == 'Deposit':
            if account_balance + int(action_value) > ACCOUNT_MAX_BALANCE:
                raise ValidationError("value of transaction in not valid")
        else:
            if account_balance - int(action_value) < ACCOUNT_MIN_BALANCE:
                raise ValidationError("value of transaction in not valid")

    @transaction.atomic
    def perform_desposit_and_withdrawal(self, data):
        self.serializer = self.get_serializer(data=data)
        self.serializer.is_valid(raise_exception=True)
        account = Account.objects.select_for_update().get(pk=data['account'])
        self.validate_desposit_and_withdrawal(account.balance, data['value'], data['type'])
        if data['type'] == 'Deposit':
            account.balance += int(data['value'])
        else:
            account.balance -= int(data['value'])
        account.owner.balance = account.balance
        account.save()
        account.owner.save()
        self.serializer.save()
        self.headers = self.get_success_headers(self.serializer.data)

    @transaction.atomic
    def perform_trasfer(self, data):
        self.serializer = self.get_serializer(data=data)
        self.serializer.is_valid(raise_exception=True)

        if not data["source"]:
            raise ValidationError("source of transfer can't be null")
        account = Account.objects.select_for_update().get(pk=data['account'])
        source = Account.objects.select_for_update().get(pk=data['source'])
        self.validate_transfer(account.balance, source.balance, data['value'])

        account.balance += int(data['value'])
        account.save()
        account.owner.balance = account.balance
        account.owner.save()
        source.balance -= int(data['value'])
        source.save()
        source.owner.balance = source.balance
        source.owner.save()
        self.serializer.save()
        self.headers = self.get_success_headers(self.serializer.data)

    def create(self, request, *args, **kwargs):
        if request.data['type'] in ('Deposit', 'Withdrawal'):
            self.perform_desposit_and_withdrawal(request.data)
            return Response(self.serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)
        elif request.data['type'] == 'Transfer':
            self.perform_trasfer(request.data)
            return Response(self.serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)
        else:
            raise ValidationError("wrong transaction type")
