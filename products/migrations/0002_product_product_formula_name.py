# Generated by Django 3.2.7 on 2021-11-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_formula_name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]