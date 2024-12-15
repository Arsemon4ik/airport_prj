from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page, name='main'),
    # path('tickets', views.user_tickets, name='user_tickets'),
    # path('tickets/book', views.user_tickets, name='book_ticket'),
    # path('tickets/<int:article_id>', views.edit_ticket_page, name='edit_ticket'),
    # path('tickets/delete/<int:article_id>', views.delete_ticket, name='delete_ticket'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
