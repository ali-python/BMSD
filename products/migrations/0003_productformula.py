# Generated by Django 3.2.7 on 2021-11-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_product_formula_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFormula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('product_formula_name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('status_available', models.BooleanField(default=True)),
            ],
        ),
    ]
