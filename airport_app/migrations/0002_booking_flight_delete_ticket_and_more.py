# Generated by Django 5.0 on 2024-12-16 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_name', models.CharField(max_length=100)),
                ('passenger_email', models.EmailField(max_length=254)),
                ('seat_class', models.CharField(choices=[('economy', 'Economy'), ('business', 'Business')], default='economy', max_length=20)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10, unique=True)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('economy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('business_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AddField(
            model_name='baggage',
            name='additional_baggage_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='baggage',
            name='baggage_type',
            field=models.CharField(choices=[('carry_on', 'Carry-on'), ('checked', 'Checked')], default='checked', max_length=20),
        ),
        migrations.AddField(
            model_name='baggage',
            name='total_weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='booking',
            name='baggage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport_app.baggage'),
        ),
        migrations.AddField(
            model_name='booking',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airport_app.flight'),
        ),
    ]