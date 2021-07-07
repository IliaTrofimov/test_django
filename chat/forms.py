from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 



class MessageForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Leave your message here'}))


class UsernameForm(forms.Form):
	username = forms.CharField(label='Username')
