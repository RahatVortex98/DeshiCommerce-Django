
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','username','is_active',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ('password', 'date_joined', 'last_login') 