# Generated by Django 5.0 on 2024-12-17 16:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_management', '0004_remove_booking_status_alter_booking_booking_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=79),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
