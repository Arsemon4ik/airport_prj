from django.contrib import admin
from .models import (
    Passenger,
    Payment,
    Baggage,
    Booking,
    BoardingPass)

# Register your models here.
admin.site.register(Passenger)
admin.site.register(Payment)
admin.site.register(Baggage)
admin.site.register(Booking)
admin.site.register(BoardingPass)