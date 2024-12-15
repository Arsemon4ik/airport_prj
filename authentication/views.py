from django.shortcuts import render, redirect

from .filters import UserFilter
from .forms import UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


def register_page(request):
    """ Register function returns register page """
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, f'Виникла помилка під час реєстрації\n{form.errors}')
    return render(request, 'authentication/register.html', {'form': form})


def login_page(request):
    """ Login function returns login page """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Виникла помилка під час авторизації')
    return render(request, 'authentication/login.html', {})


@login_required
def my_profile_page(request):
    """ My profile function returns user profile page """
    user = request.user

    form = UserProfileForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.update(bio=form.cleaned_data["bio"])
            return redirect('my_profile')
        else:
            messages.error(request, f'Виникла помилка {form.errors} під час редагування, спробуйте ще раз')
    return render(request, 'authentication/my_profile.html', {'form': form})


def profile_page(request, user_id):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    user = User.objects.filter(id=user_id).first()
    user_articles = user.article_set.all()
    return render(request, 'authentication/profile.html', {'user': user, 'articles': user_articles})


def search_users_page(request):
    """ Subject function returns a template with subjects and tasks from DB based on user """
    f = UserFilter(queryset=None)
    if request.method == "GET":
        f = UserFilter(request.GET, queryset=User.objects.all())
    return render(request, 'authentication/search_users.html', {'filter': f})


@login_required
def logout_page(request):
    """ Logout function returns logout user """
    logout(request)
    return redirect('main')
