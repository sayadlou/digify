import re
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from .validator import is_valid_iran_code, is_valid_mobile_number
from ..credit.policy import ACCOUNT_MIN_BALANCE, ACCOUNT_MAX_BALANCE
from ..debit.policy import LOAN_MIN_VALUE, LOAN_MAX_VALUE, LOAN_MAX_DIGITS


class Client(models.Model):
    """Client model for saving information of client in bank """
    STATUS = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default='Open')
    national_id = models.CharField(max_length=10, unique=True, validators=[is_valid_iran_code])
    mobile_number = models.CharField(max_length=11, unique=True, validators=[is_valid_mobile_number])
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0,
                                  validators=[MinValueValidator(ACCOUNT_MIN_BALANCE),
                                              MaxValueValidator(ACCOUNT_MAX_BALANCE)])
    total_loan = models.DecimalField(max_digits=LOAN_MAX_DIGITS, decimal_places=0, default=0,
                                     validators=[MinValueValidator(LOAN_MIN_VALUE), MaxValueValidator(LOAN_MAX_VALUE)])
    total_debit = models.DecimalField(max_digits=LOAN_MAX_DIGITS, decimal_places=0, default=0,
                                      validators=[MinValueValidator(LOAN_MIN_VALUE), MaxValueValidator(LOAN_MAX_VALUE)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
