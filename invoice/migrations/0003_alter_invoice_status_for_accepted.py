# Generated by Django 3.2.7 on 2021-11-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_invoicenotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status_for_accepted',
            field=models.BooleanField(default=False),
        ),
    ]