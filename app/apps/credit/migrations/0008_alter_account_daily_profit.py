# Generated by Django 3.2.10 on 2022-01-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0007_account_daily_profit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='daily_profit',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=12),
        ),
    ]
