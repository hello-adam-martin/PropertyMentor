from django.contrib import admin
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')