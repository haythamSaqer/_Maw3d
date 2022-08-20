from django.contrib import admin
from .models import Profile, UserAccount,Availability


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAccount

    inlines = [ProfileInline]

admin.site.register([Availability])
