import uuid
import shortuuid
from django.db import models
from datetime import timedelta
from authentication.models import User


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    managed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="passengers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Baggage(models.Model):
    # Багаж
    total_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Вага
    baggage_type = models.CharField(
        max_length=20,
        choices=[('carry_on', 'Carry-on'), ('checked', 'Checked')],
        default='checked',
    )
    additional_baggage_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Flight(models.Model):
    # Рейс
    flight_number = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    origin = models.CharField(max_length=100)  # Місто відправлення
    destination = models.CharField(max_length=100)  # Місто призначення
    departure_time = models.DateTimeField()  # Час відправлення
    arrival_time = models.DateTimeField()  # Час прибуття
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна за економ
    business_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна за бізнес

    def save(self, *args, **kwargs):
        # Generate a unique flight number if it doesn't already exist
        if not self.flight_number:
            self.flight_number = self._generate_flight_number()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        # Calculate and return the duration in hours and minutes
        delta = self.arrival_time - self.departure_time
        hours, minutes = divmod(delta.seconds // 60, 60)
        return f"{hours}h {minutes} min"

    def _generate_flight_number(self):
        """
        Generate a unique flight number using shortuuid, with a custom prefix.
        """
        prefix = "FL"  # Static prefix for flight numbers
        unique_id = uuid.uuid4()  # Generate a random 6-character ID
        return f"{prefix}-{unique_id}"

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Baggage class.
        :return: class, id
        """
        return f"{Flight.__name__}(id={self.id})"


class Booking(models.Model):
    # Бронювання
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    booking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    booking_status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=79)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="bookings")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")  # Зв’язок з рейсом
    baggage = models.ForeignKey(Baggage, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    seat_class = models.CharField(
        max_length=20,
        choices=[('economy', 'Economy'), ('business', 'Business')],
        default='economy',
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique flight number if it doesn't already exist
        if not self.booking_code:
            self.booking_code = self._generate_booking_code()
        super().save(*args, **kwargs)

    def _generate_booking_code(self):
        """
        Generate a unique booking code.
        """
        unique_id = uuid.uuid4()
        return f"{unique_id}"

    def __str__(self):
        return f"Booking for {self.passenger.email} on flight {self.flight.flight_number}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Booking class.
        :return: class, id
        """
        return f"{Booking.__name__}(id={self.id})"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')]
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    def __str__(self):
        return f"Payment for Booking {self.booking.booking_code} - {self.payment_status}"


class BoardingPass(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='boarding_pass')
    gate = models.CharField(max_length=10)
    boarding_time = models.DateTimeField()
    qr_code = models.ImageField(upload_to='boarding_passes/qrcodes/', null=True, blank=True)

    def __str__(self):
        return f"Boarding Pass for {self.booking.passenger}"

    @classmethod
    def generate_boarding_pass(cls, booking):
        """
        Generates a boarding pass for a booking if payment is completed.
        """
        gate = "G1" if booking.seat_class == "economy" else "G2"
        if booking.payment.payment_status == 'Completed':
            return cls.objects.create(
                booking=booking,
                gate=gate,
                boarding_time=booking.flight.departure_time - timedelta(minutes=30)
            )
        else:
            raise ValueError("Boarding pass cannot be generated. Payment is not completed.")
