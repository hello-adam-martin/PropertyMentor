from django.contrib import admin
from .models import Owner

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('date_joined',)