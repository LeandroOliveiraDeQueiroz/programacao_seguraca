from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=200)
    password = forms.CharField(label='password', max_length=200)
    password_confirm = forms.CharField(label='password_confirm', max_length=200, required=False)
    totp_token = forms.CharField(label='totp_token', max_value=6, required=False)
