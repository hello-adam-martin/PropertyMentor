from django.contrib import admin
from .models import Property, PricingRule, BookingRule

class PricingRuleInline(admin.TabularInline):
    model = PricingRule
    extra = 1
    fields = ('rule_type', 'start_date', 'end_date', 'price_modifier')

class BookingRuleInline(admin.TabularInline):
    model = BookingRule
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'bedrooms', 'bathrooms', 'nightly_rate')
    list_filter = ('bedrooms', 'bathrooms')
    search_fields = ('name', 'address', 'owner__first_name', 'owner__last_name')
    inlines = [PricingRuleInline, BookingRuleInline]

@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('property', 'rule_type', 'start_date', 'end_date', 'price_modifier_display')
    list_filter = ('rule_type', 'property')
    search_fields = ('property__name',)

    def price_modifier_display(self, obj):
        return f"{obj.price_modifier}%"
    price_modifier_display.short_description = 'Price Modifier'

@admin.register(BookingRule)
class BookingRuleAdmin(admin.ModelAdmin):
    list_display = ('property', 'rule_type', 'start_date', 'end_date', 'min_nights')
    list_filter = ('rule_type', 'property')
    search_fields = ('property__name',)