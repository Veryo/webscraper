from django import forms

class UrlForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)