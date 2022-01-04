from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.client.models import Client
from apps.credit.Policy import TRANSACTION_MIN_VALUE, TRANSACTION_MAX_VALUE, TRANSACTION_MAX_DIGITS, \
    ACCOUNT_MIN_BALANCE, ACCOUNT_MAX_BALANCE, ACCOUNT_MAX_DIGITS


class Account(models.Model):
    """credit model for saving information of client credit"""
    STATUS = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.OneToOneField(Client, on_delete=models.RESTRICT)
    balance = models.DecimalField(max_digits=ACCOUNT_MAX_DIGITS, decimal_places=0, default=0,
                                  validators=[MinValueValidator(ACCOUNT_MIN_BALANCE),
                                              MaxValueValidator(ACCOUNT_MAX_BALANCE)])
    status = models.CharField(max_length=20, choices=STATUS, default="Open")

    def __str__(self):
        return f'{self.owner.first_name} {self.owner.last_name} {self.owner.national_id}'


class Transaction(models.Model):
    """transaction model for transaction of client credit"""
    TYPE = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="account")
    type = models.CharField(max_length=10, choices=TYPE)
    source = models.ForeignKey(Account, on_delete=models.RESTRICT, null=True, blank=True, related_name="source")
    value = models.DecimalField(max_digits=TRANSACTION_MAX_DIGITS, decimal_places=0, default=0,
                                validators=[MinValueValidator(TRANSACTION_MIN_VALUE),
                                            MaxValueValidator(TRANSACTION_MAX_VALUE)])
    creat_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'
