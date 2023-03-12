from django import forms

class UrlForm(forms.Form):
    id = forms.CharField(label='ID', max_length=100)