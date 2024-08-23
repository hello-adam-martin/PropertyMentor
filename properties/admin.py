from django.contrib import admin
from .models import Property, PricingRule

class PricingRuleInline(admin.TabularInline):
    model = PricingRule
    extra = 1
    fields = ('rule_type', 'start_date', 'end_date', 'price_modifier')

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'price_modifier' in fields:
            index = fields.index('price_modifier')
            fields[index] = admin.models.PercentageField('price_modifier')
        return fields

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'bedrooms', 'bathrooms', 'nightly_rate')
    list_filter = ('bedrooms', 'bathrooms')
    search_fields = ('name', 'address', 'owner__first_name', 'owner__last_name')
    inlines = [PricingRuleInline]

@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('property', 'rule_type', 'start_date', 'end_date', 'price_modifier_display')
    list_filter = ('rule_type', 'property')
    search_fields = ('property__name',)

    def price_modifier_display(self, obj):
        return f"{obj.price_modifier}%"
    price_modifier_display.short_description = 'Price Modifier'