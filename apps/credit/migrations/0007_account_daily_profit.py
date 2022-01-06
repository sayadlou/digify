# Generated by Django 3.2.10 on 2022-01-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0006_alter_transaction_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='daily_profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]