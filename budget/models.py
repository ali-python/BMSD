from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum
import random
from django.db.models.signals import post_save
from common.models import DatedModel
from django.utils import timezone
from common.models import District


class BmsdBudget(models.Model):
    budget_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text="Budget amount 100000"
    )
    discription = models.CharField(max_length=200, null=True, blank=True)
    document = models.ImageField(
        upload_to="user/files/", null=True, blank=True
    )
    start_dated = models.DateField(blank=True, null=True)
    end_dated = models.DateField(blank=True, null=True)
    dated = models.DateField(default=timezone.now, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __unicode__ (self):
        return  self.budget_amount

class BudgetUtilizeDistrict(models.Model):
	utilize_total_budget = models.ForeignKey(
		BmsdBudget, related_name='utilize_budget_district', on_delete=models.CASCADE, null=True, blank=True)
	district = models.ForeignKey(District, related_name='district_budget', on_delete=models.CASCADE,
		null=True, blank=True)
	district_budget_amount = models.DecimalField(max_digits=65, default=0, decimal_places=2,
	 blank=True, null=True)
	discription = models.CharField(max_length=200, null=True, blank=True)
	start_dated = models.DateField(blank=True, null=True)
	end_dated = models.DateField(blank=True, null=True)
	dated = models.DateField(default=timezone.now, blank=True, null=True)
	status = models.BooleanField(default=False)

	def __unicode__(self):
		return self.discription

class ReviseBudgetDistrict(models.Model):
	previous_budget_record = models.ForeignKey(BudgetUtilizeDistrict, related_name='utilize_previous_budget',
	 on_delete=models.CASCADE, null=True, blank=True)
	revise_budget_amount = models.DecimalField(max_digits=65, default=0, decimal_places=2, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	start_dated = models.DateField(null=True, blank=True)
	end_dated = models.DateField(null=True, blank=True)
	dated = models.DateField(default=timezone.now, null=True, blank=True)

	def __unicode__(self):
		return self.previous_budget_record.district.name




