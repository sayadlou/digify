from time import sleep
from celery import shared_task
from kavenegar import *
import os

from .models import Account


@shared_task
def notify_customers(sms):
    api_key = os.environ.get('kavenegar_api_key')
    api = KavenegarAPI(api_key)
    params = {'sender': '100047778', 'receptor': sms['mobile_number'], 'message': sms['content']}
    print(api.sms_send(params))


@shared_task
def daily_profit_calculate():
    Account.daily_calculate_profit()
    print("daily profit of accounts calculated")


@shared_task
def yearly_profit_apply():
    Account.apply_profit()
    print("profit of accounts applied")


@shared_task
def test():
    print("test done")
