from django.db import models


class Flight(models.Model):
    # Рейс
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)  # Місто відправлення
    destination = models.CharField(max_length=100)  # Місто призначення
    departure_time = models.DateTimeField()  # Час відправлення
    arrival_time = models.DateTimeField()  # Час прибуття
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна за економ
    business_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна за бізнес

    def __str__(self):
        return f"{self.flight_number} - {self.origin} to {self.destination}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Baggage class.
        :return: class, id
        """
        return f"{Flight.__name__}(id={self.id})"


class Baggage(models.Model):
    # Багаж
    total_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Вага
    baggage_type = models.CharField(
        max_length=20,
        choices=[('carry_on', 'Carry-on'), ('checked', 'Checked')],
        default='checked',
    )
    additional_baggage_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        """
        Magic method is redefined to show all information about Baggage
        :return: subject id and theme
        """
        return f"Baggage {self.id} {self.baggage_type}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Baggage class.
        :return: class, id
        """
        return f"{Baggage.__name__}(id={self.id})"


class Booking(models.Model):
    # Бронювання
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Зв’язок з рейсом
    baggage = models.ForeignKey(Baggage, on_delete=models.CASCADE)  # Зв’язок з рейсом
    seat_class = models.CharField(
        max_length=20,
        choices=[('economy', 'Economy'), ('business', 'Business')],
        default='economy',
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)  # Статус оплати

    def __str__(self):
        return f"Booking for {self.passenger_name} on flight {self.flight.flight_number}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Booking class.
        :return: class, id
        """
        return f"{Booking.__name__}(id={self.id})"
