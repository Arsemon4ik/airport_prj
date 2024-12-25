from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Passenger, Flight, Booking, Baggage
from .forms import PassengerForm, BookingForm, BaggageFormSet


@login_required
def add_passenger(request):
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)  # Create instance but don't save yet
            if passenger.email != request.user.email:  # Check if passenger is not a user
                passenger.managed_by = request.user  # Set the current user as the manager
            passenger.save()
            return redirect('my_profile')
    else:
        form = PassengerForm()

    return render(request, 'booking_management/add_passenger.html', {'form': form})


@login_required
def update_passenger(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)

    if request.method == "POST":
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()  # Save updates without changing `managed_by`
            return redirect('my_profile')
    else:
        form = PassengerForm(instance=passenger)

    return render(request, 'booking_management/edit_passenger.html', {'form': form})


@login_required
def delete_passenger(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)
    if request.method == 'POST':
        passenger.delete()
        return redirect('my_profile')

    return render(request, 'authentication/my_profile.html', {'passenger': passenger})


@login_required
def list_passengers(request):
    passengers = Passenger.objects.filter(managed_by=request.user)  # Filter by the logged-in user
    return render(request, 'authentication/my_profile.html', {'passengers': passengers})


def flight_list(request):
    flights = Flight.objects.all()

    # Filters
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if origin:
        flights = flights.filter(origin__icontains=origin)
    if destination:
        flights = flights.filter(destination__icontains=destination)
    if min_price:
        flights = flights.filter(economy_price__gte=min_price)
    if max_price:
        flights = flights.filter(economy_price__lte=max_price)
    if min_price:
        flights = flights.filter(business_price__gte=min_price)
    if max_price:
        flights = flights.filter(business_price__lte=max_price)

    context = {
        'flights': flights,
        'filters': {
            'origin': origin or '',
            'destination': destination or '',
            'min_price': min_price or '',
            'max_price': max_price or '',
        }
    }
    return render(request, 'booking_management/flights.html', context)


# List all bookings
def booking_list(request):
    bookings = Booking.objects.all()

    # Filters
    booking_status = request.GET.get('booking_status')
    seat_class = request.GET.get('seat_class')

    if booking_status:
        bookings = bookings.filter(booking_status__icontains=booking_status)
    if booking_status:
        bookings = bookings.filter(seat_class__icontains=seat_class)

    context = {
        'bookings': bookings,
        'filters': {
            'booking_status': booking_status or '',
            'seat_class': booking_status or '',
        }
    }
    return render(request, 'booking_management/bookings.html', context)


# View booking details
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking_management/booking_detail.html', {'booking': booking})


# Create a new booking
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        formset = BaggageFormSet(request.POST, queryset=Baggage.objects.none())  # Новий набір форм

        if form.is_valid() and formset.is_valid():
            # Збереження бронювання
            booking = form.save(commit=False)

            # Збереження багажу та прив'язка до бронювання
            for baggage_form in formset:
                if baggage_form.cleaned_data and not baggage_form.cleaned_data.get('DELETE'):  # Уникаємо порожніх форм
                    baggage = baggage_form.save()
                    baggage.save()
                    booking.baggage = baggage
            booking.save()# Прив'язуємо до бронювання

            return redirect('booking_list')  # Перенаправлення після успіху
    else:
        form = BookingForm()
        formset = BaggageFormSet(queryset=Baggage.objects.none())  # Порожній набір форм

    return render(request, 'booking_management/booking_create.html', {
        'form': form,
        'formset': formset,
    })

# Update an existing booking
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking_management/booking_edit.html', {'form': form})


# Delete a booking
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'booking_management/bookings.html', {'booking': booking})
