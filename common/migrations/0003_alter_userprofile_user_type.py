# Generated by Django 3.2.7 on 2021-11-08 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20211105_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('Director', 'Director'), ('DHO', 'DHO'), ('store_keeper', 'store_keeper'), ('data_entry_operator', 'data_entry_operator')], default='Director', max_length=100),
        ),
    ]
