from django.contrib import admin

from .models import BmsdBudget, BudgetUtilizeDistrict, ReviseBudgetDistrict

class BmsdBudgetAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'discription', 'document', 'start_dated',
        'end_dated', 'dated', 'status'
    )
    search_fields = (
        'start_dated', 'end_dated',
    )


class BudgetUtilizeDistrictAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'utilize_total_budget', 'district', 'district_budget_amount', 'discription',
        'start_dated', 'end_dated', 'dated', 'status'
    )
    search_fields = (
        'start_dated', 'end_dated',
    )


class ReviseBudgetDistrictAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'previous_budget_record', 'revise_budget_amount', 'description', 'start_dated',
        'end_dated', 'dated'
    )
    search_fields = (
        'start_dated', 'end_dated',
    )
admin.site.register(BmsdBudget, BmsdBudgetAdmin)
admin.site.register(BudgetUtilizeDistrict, BudgetUtilizeDistrictAdmin)
admin.site.register(ReviseBudgetDistrict, ReviseBudgetDistrictAdmin)

