from django.forms import ModelForm, TextInput, Select
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['owner', 'time_added', 'highest_bid', 'on_market']
        labels = {
            'title': 'Title:', 
            'starting_bid': 'Starting bid (USD): ',
            'caregory': 'Product category: ',
            'picture' : 'Upload picture of product: '
            }

        widgets = {
            'title': TextInput(attrs={'placeholder': 'Enter title', 'autofocus': True}),
            'starting_bid': TextInput(attrs={'type': 'number',}),
            'category': Select(attrs={'placeholder': 'Enter category'}),
        }        


