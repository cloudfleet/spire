from django import forms

class RequestCertificateForm(forms.Form):
    domain = forms.CharField(max_length=200)
    secret = forms.PasswordInput()
    signature = forms.FileField()
