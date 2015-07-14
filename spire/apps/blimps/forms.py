from django import forms

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
