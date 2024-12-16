from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Passenger
from .forms import PassengerForm


@login_required
def add_passenger(request):
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)  # Create instance but don't save yet
            if passenger.email != request.user.email: # Check if passenger is not a user
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
