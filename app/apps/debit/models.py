from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.client.models import Client
from apps.credit.policy import TRANSACTION_MIN_VALUE, TRANSACTION_MAX_VALUE, TRANSACTION_MAX_DIGITS, ACCOUNT_MAX_DIGITS
from apps.debit.policy import LOAN_MAX_DIGITS, LOAN_MIN_VALUE

from apps.debit.policy import LOAN_MAX_VALUE


class Loan(models.Model):
    """credit model for saving information of client credit"""
    STATUS = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )
    TOTAL_INSTALLMENT = (
        (12, 12),
        (24, 24)
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(Client, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=LOAN_MAX_DIGITS, decimal_places=0, default=0,
                                 validators=[MinValueValidator(LOAN_MIN_VALUE),
                                             MaxValueValidator(LOAN_MAX_VALUE)])
    remained_amount = models.DecimalField(max_digits=ACCOUNT_MAX_DIGITS, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS, default="Open")
    total_installment = models.IntegerField(choices=TOTAL_INSTALLMENT)
    remained_installment = models.IntegerField()
    branch = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return f'Loan {self.owner.first_name} {self.owner.last_name} {self.owner.national_id}'
