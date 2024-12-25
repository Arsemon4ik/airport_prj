import json

from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Passenger, Flight, Booking, Baggage
from .forms import PassengerForm, BookingForm, BaggageFormSet
import logging
from django.contrib import messages

from .utils import MonoBankService, send_order_confirmation_email

logger = logging.getLogger(__name__)


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
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(passenger__managed_by=request.user)

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
        formset = BaggageFormSet(request.POST, queryset=Baggage.objects.none())

        monobank_client = MonoBankService()
        total = 0

        if form.is_valid() and formset.is_valid():
            # Save the booking
            booking = form.save()
            flight = booking.flight

            if booking.seat_class == 'economy':
                ticket_price = flight.economy_price
            elif booking.seat_class == 'business':
                ticket_price = flight.business_price
            else:
                ticket_price = 0

            total += ticket_price

            for baggage_form in formset:
                if baggage_form.cleaned_data and not baggage_form.cleaned_data.get('DELETE'):
                    baggage = baggage_form.save(commit=False)

                    if baggage.total_weight > 20:
                        baggage.additional_baggage_fee = (baggage.total_weight - 20) * 20  # 1кг / 20 грн дод.плата
                    else:
                        baggage.additional_baggage_fee = 0
                    total += baggage.additional_baggage_fee
                    baggage.save()

                    booking.baggage = baggage

                booking.total_price = total
                booking.save()

            description = f"Сплата за квиток {flight.flight_number}"
            payment_url = monobank_client.create_invoice(booking.booking_code, description, total)
            print(payment_url)
            if payment_url:
                return redirect(payment_url)
            else:
                messages.error(request, f'Виникла помилка під час створення платежу')
        else:
            messages.error(request, f'Виникла помилка під час створення квитка: {form.errors} {formset.errors}')
    else:
        form = BookingForm()
        formset = BaggageFormSet(queryset=Baggage.objects.none())

    return render(request, 'booking_management/booking_create.html', {
        'form': form,
        'formset': formset,
    })


@csrf_exempt
def monopay_callback(request):
    if request.method != 'POST':
        logger.error(f'{request.method} in mono_checkout_callback is not allowed! \n{request.body}')
        return JsonResponse({"message": f"{request.method} is not allowed in Callback"}, status=200)
    try:
        data = json.loads(request.body)
        if not data:
            logger.error(f'No data in call-back function mono_checkout_callback, request: \n{request.body}')
            return JsonResponse({"message": "Callback received and processed"}, status=200)

        status = data.get("status")
        if status not in ['success', 'payment_on_delivery']:
            return JsonResponse({"message": "Callback received and processed"}, status=200)

        booking_ref = data.get("reference")

        try:
            booking = Booking.objects.get(booking_code=booking_ref)
        except Booking.DoesNotExist:
            logger.error(f'Error order not found with order_ref: {booking_ref}')
            return JsonResponse({"error": "Order not found"}, status=404)

        if booking.booking_status == 'Confirmed':
            return JsonResponse({"message": "Booking has already confirmed"}, status=404)

        if status == 'success':
            booking.booking_status = 'Confirmed'
            booking.save()
            send_order_confirmation_email(booking)
        return JsonResponse({"message": "Callback received and processed"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.error(f'Error while trying to send email for order ref: {e}')
        return JsonResponse({"error": 'Server error during call-back'}, status=500)


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
