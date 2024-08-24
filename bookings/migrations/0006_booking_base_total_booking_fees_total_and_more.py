# Generated by Django 5.1 on 2024-08-24 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_alter_booking_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='base_total',
            field=models.DecimalField(decimal_places=2, default=100, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='fees_total',
            field=models.DecimalField(decimal_places=2, default=100, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='num_guests',
            field=models.PositiveIntegerField(default=4),
            preserve_default=False,
        ),
    ]
