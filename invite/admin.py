from django.contrib import admin
from .models import Invite, Availability

# Register your models here.
admin.site.register([Invite, Availability])
