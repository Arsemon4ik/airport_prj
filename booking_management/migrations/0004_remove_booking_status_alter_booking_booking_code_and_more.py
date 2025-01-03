# Generated by Django 5.0 on 2024-12-17 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_management', '0003_alter_passenger_managed_by_alter_passenger_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_code',
            field=models.UUIDField(blank=True, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='flight_number',
            field=models.CharField(blank=True, editable=False, max_length=10, unique=True),
        ),
    ]
