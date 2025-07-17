from django import forms

from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Ton nom'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Ton mot de passe'
        })
    )
