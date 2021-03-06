from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Contest, Profile, Stock, StockEntry, Request, HeadToHeadMatch



# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton

class MembershipInline(admin.TabularInline):
    model = Request.stocks.through

class RequestAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Contest)
admin.site.register(Stock)
admin.site.register(StockEntry)
admin.site.register(Request, RequestAdmin)
admin.site.register(HeadToHeadMatch)