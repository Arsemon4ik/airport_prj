from django.contrib import admin
from .models import (
    Passenger,
    Payment,
    Baggage,
    Booking,
    BoardingPass,
    Flight
)

# Register your models here.
admin.site.register(Passenger)
admin.site.register(Payment)
admin.site.register(Baggage)
admin.site.register(Booking)
admin.site.register(BoardingPass)
admin.site.register(Flight)