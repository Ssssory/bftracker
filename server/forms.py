from django import forms
from django.forms import fields 
from .models import Point


class PointForm(forms.ModelForm):
    class Meta:
        model = Point 
        fields = ['address', 'name', 'login', 'password']
