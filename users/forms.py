from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(
        label="Nombre de usuario",
        strip=False,
        help_text='Tu nombre de usuario puede con tener 150 carácteres o menos. Letras, digítos, and @/./+/-/_  solamente',
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
        help_text='La contraseña debe contener mayúsculas, minúsculas y al menos un carácter.',
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(
        label="Nombre de usuario",
        strip=False,
        help_text='Tu nombre de usuario puede con tener 150 carácteres o menos sin espacios. Letras, digítos, y @/./+/-/_  se permiten',
    )
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
