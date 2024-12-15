from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('profile/', views.my_profile_page, name="my_profile"),
    path('profile/<int:user_id>', views.profile_page, name="profile"),
    path('profile/search', views.search_users_page, name="search_users"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
