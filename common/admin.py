from django.contrib import admin

from .models import UserProfile, District

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'district', 'first_name', 'last_name', 'phone_no',
        'email', 'user_type', 'office_address', 'city', 'dated'
    )
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'phone_no',
    )

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def email(obj):
        return obj.user.email

class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'dated'
    )
    search_fields = (
        'name',
    )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(District, DistrictAdmin)

