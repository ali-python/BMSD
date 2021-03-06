# Generated by Django 3.2.7 on 2021-11-17 08:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productformula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productformula',
            name='product_name',
        ),
        migrations.CreateModel(
            name='ProductFormulaRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_available', models.BooleanField(default=True)),
                ('dated', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('product_formula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_product_formula', to='products.productformula')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_product_name', to='products.product')),
            ],
        ),
    ]
