# Generated by Django 3.2.7 on 2021-11-08 08:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BmsdBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_amount', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Budget amount 100000', max_digits=65, null=True)),
                ('discription', models.CharField(blank=True, max_length=200, null=True)),
                ('document', models.ImageField(blank=True, null=True, upload_to='user/files/')),
                ('start_dated', models.DateField(blank=True, null=True)),
                ('end_dated', models.DateField(blank=True, null=True)),
                ('dated', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetUtilizeDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_budget_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('discription', models.CharField(blank=True, max_length=200, null=True)),
                ('start_dated', models.DateField(blank=True, null=True)),
                ('end_dated', models.DateField(blank=True, null=True)),
                ('dated', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district_budget', to='common.district')),
                ('utilize_total_budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utilize_budget_district', to='budget.bmsdbudget')),
            ],
        ),
        migrations.CreateModel(
            name='ReviseBudgetDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revise_budget_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_dated', models.DateField(blank=True, null=True)),
                ('end_dated', models.DateField(blank=True, null=True)),
                ('dated', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('previous_budget_record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='utilize_previous_budget', to='budget.budgetutilizedistrict')),
            ],
        ),
    ]
