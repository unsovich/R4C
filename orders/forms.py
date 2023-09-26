from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    robot_serial = forms.CharField(max_length=5)

    class Meta:
        model = Order
        fields = ['robot_serial', 'customer']
