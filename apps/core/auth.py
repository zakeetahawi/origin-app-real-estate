"""
Authentication views for the application
"""
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with Bootstrap styling"""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم / Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور / Password'
        })
    )


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'auth/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('core:dashboard')


class CustomLogoutView(TemplateView):
    """Custom logout view that handles both GET and POST"""
    template_name = 'auth/logout.html'
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Show logout confirmation page"""
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Log out the user and redirect"""
        logout(request)
        return redirect('core:login')
