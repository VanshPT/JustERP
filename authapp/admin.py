from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CompanyProfile, CustomUser
# Register your models here.
admin.site.register(CompanyProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'type', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)