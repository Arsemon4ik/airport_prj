from django.urls import path
from . import views

# Create your views here.
# /booking/create/
# /booking/edit/<int:pk>/
# /booking/boarding-pass/<int:pk>/
urlpatterns = [
    # Passenger-related URLs
    path('passenger/add/', views.add_passenger, name='add_passenger'),
    path('passenger/list/', views.list_passengers, name='list_passengers'),
    path('passenger/update/<int:passenger_id>/', views.update_passenger, name='update_passenger'),
    path('passenger/delete/<int:passenger_id>/', views.delete_passenger, name='delete_passenger'),
]