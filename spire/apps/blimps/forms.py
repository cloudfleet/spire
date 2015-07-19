from django import forms
from django.forms import ModelForm
from .models import Blimp

class BlimpForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['domain']

class RequestCertificateForm(forms.Form):
    domain = forms.CharField(max_length=200)
    secret = forms.PasswordInput()
    signature = forms.FileField()

class RequestCertificateJSONForm(forms.Form):
    domain = forms.CharField(max_length=200)
    secret = forms.PasswordInput()
    cert_req = forms.CharField()

class GetCertificateForm(forms.Form):
    domain = forms.CharField(max_length=200)
    secret = forms.PasswordInput()

# new API

class BlimpAPIForm(ModelForm):
    class Meta:
        model = Blimp
        fields = ['domain', 'username', 'password']

class BlimpAPICertificateRequestForm(forms.Form):
    cert_req = forms.CharField()
    OTP = forms.CharField()
