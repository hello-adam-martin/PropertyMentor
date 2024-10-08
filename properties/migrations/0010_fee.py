# Generated by Django 5.1 on 2024-08-24 00:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_alter_bookingrule_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fee_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], max_length=10)),
                ('applies', models.CharField(choices=[('per_night', 'Every Night'), ('once', 'Once per Stay')], max_length=10)),
                ('display_strategy', models.CharField(choices=[('separate', 'Show Separately'), ('incorporated', 'Incorporate into Price')], max_length=12)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_extra_guest_fee', models.BooleanField(default=False)),
                ('extra_guest_threshold', models.PositiveIntegerField(blank=True, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='properties.property')),
            ],
            options={
                'unique_together': {('property', 'name')},
            },
        ),
    ]
