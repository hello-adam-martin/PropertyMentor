from django.contrib import admin
from django import forms
from .models import Property, PricingRule, BookingRule, Fee

class PropertyAdminForm(forms.ModelForm):
    no_checkin_days = forms.MultipleChoiceField(
        choices=Property.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    no_checkout_days = forms.MultipleChoiceField(
        choices=Property.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Property
        fields = '__all__'

    def clean_no_checkin_days(self):
        return ''.join(self.cleaned_data['no_checkin_days'])

    def clean_no_checkout_days(self):
        return ''.join(self.cleaned_data['no_checkout_days'])

class PricingRuleInline(admin.TabularInline):
    model = PricingRule
    extra = 1

class BookingRuleInline(admin.TabularInline):
    model = BookingRule
    extra = 1

class FeeInline(admin.TabularInline):
    model = Fee
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    list_display = ('name', 'address', 'owner', 'bedrooms', 'bathrooms', 'nightly_rate', 'minimum_stay')
    list_filter = ('bedrooms', 'bathrooms', 'minimum_stay')
    search_fields = ('name', 'address', 'owner__first_name', 'owner__last_name')
    inlines = [PricingRuleInline, BookingRuleInline, FeeInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['no_checkin_days'].initial = list(obj.no_checkin_days)
            form.base_fields['no_checkout_days'].initial = list(obj.no_checkout_days)
        return form

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'fee_type', 'applies', 'display_strategy', 'amount', 'is_extra_guest_fee')
    list_filter = ('fee_type', 'applies', 'display_strategy', 'is_extra_guest_fee')
    search_fields = ('name', 'property__name')