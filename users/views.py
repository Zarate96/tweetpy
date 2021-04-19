import urllib.request
import json

from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            
            if result['success']:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Tu cuenta ha sido creada! {username}! Ahora pudes inciar sesión')
                return redirect('login')
            else:
                messages.success(request, f'Recaptcha no válido o no seleccionado')
                form = UserRegisterForm()
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Tu cuenta ha sido actualizada!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'users': User.objects.all()
    }
    return render(request, 'users/profile.html', context)
