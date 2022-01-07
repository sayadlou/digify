"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

from apps.branch.views import CustomAuthToken, RegisterView
from apps.client.views import ClientViewSet
from apps.credit.models import Account
from apps.credit.views import AccountViewSet, TransactionViewSet
from apps.credit.tasks import notify_customers
from apps.debit.views import LoanViewSet

router = DefaultRouter()
router.register('client', ClientViewSet)
router.register('branch', RegisterView)
router.register('account', AccountViewSet)
router.register('transaction', TransactionViewSet)
router.register('loan', LoanViewSet)


def celery(request):
    notify_customers.delay("salam")
    return HttpResponse("done")


urlpatterns = [
    path('apiv1/', include(router.urls)),
    path("apiv1/login", CustomAuthToken.as_view()),
    path("task", celery),

]
