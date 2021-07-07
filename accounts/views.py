from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        return reverse('accounts:signin')


class SigninView(LoginView):
    template_name = 'accounts/signin.html'

    def get_success_url(self):
        return reverse('chat:index')


def signout(request):
    logout(request)
    return redirect('chat:index')
