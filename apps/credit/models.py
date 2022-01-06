from datetime import datetime
from calendar import isleap
from decimal import Decimal
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction

from apps.client.models import Client
from apps.credit.policy import TRANSACTION_MIN_VALUE, TRANSACTION_MAX_VALUE, TRANSACTION_MAX_DIGITS, \
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
    daily_profit = models.DecimalField(max_digits=ACCOUNT_MAX_DIGITS, decimal_places=5, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="Open")
    branch = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.owner.first_name} {self.owner.last_name} {self.owner.national_id}'

    @classmethod
    def daily_calculate_profit(cls):
        all_account_obj = []
        day_of_year = 365 + isleap(datetime.now().year)
        for account in cls.objects.all():
            account.daily_profit += (account.balance * Decimal('0.1')) / day_of_year
            all_account_obj.append(account)
        cls.objects.bulk_update(all_account_obj, ['daily_profit'])

    @classmethod
    def apply_profit(cls):
        all_account_obj = []
        all_account_pk = list(cls.objects.values_list('pk'))
        # print(all_account_pk)
        # print(type(all_account_pk[0]))
        with transaction.atomic():
            for pk in all_account_pk:
                account = cls.objects.select_for_update().get(pk=pk[0])
                Transaction.objects.create(
                    account=account,
                    type='Profit',
                    value=account.daily_profit

                )
                account.balance += account.daily_profit
                account.daily_profit = Decimal('0.0')
                all_account_obj.append(account)
        cls.objects.bulk_update(all_account_obj, ['daily_profit', 'balance'])


class Transaction(models.Model):
    """transaction model for transaction of client credit"""
    TYPE = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
        ('Profit', 'Profit'),
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
