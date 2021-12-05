from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DatedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class District(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    dated =models.DateField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    USER_TYPE_DIRECTOR = 'Director'
    USER_TYPE_DHO = 'DHO'
    USER_TYPE_STORE_KEEPER = 'store_keeper'
    USER_TYPE_DATA_ENTRY_OPERATOR = 'data_entry_operator'

    USER_TYPES = (
        (USER_TYPE_DIRECTOR, 'Director'),
        (USER_TYPE_DHO, 'DHO'),
        (USER_TYPE_STORE_KEEPER, 'store_keeper'),
        (USER_TYPE_DATA_ENTRY_OPERATOR, 'data_entry_operator')
    )

    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, related_name='user_district',on_delete=models.CASCADE, null=True, blank=True
    )
    user_type = models.CharField(
        max_length=100, choices=USER_TYPES, default=USER_TYPE_DIRECTOR
    )
    address = models.TextField(max_length=512, blank=True, null=True)
    office_address = models.TextField(max_length=512, blank=True, null=True)
    city = models.TextField(max_length=512, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    mobile_no = models.CharField(max_length=13, blank=True, null=True)
    picture = models.ImageField(
        upload_to='images/profile/picture/', max_length=1024, blank=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    dated =models.DateField(default=timezone.now, blank=True, null=True)

    def __unicode__(self):
        return self.user.username