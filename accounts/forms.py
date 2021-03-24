from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


message = {
    'required': 'this field is required',
    'invalid': 'please enter a valid email address',
    'ma_length': 'character for this field is too long'
}


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=77, error_messages=message, widget=forms.TextInput())
    email = forms.EmailField(max_length=77, error_messages=message, widget=forms.TextInput())
    password = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput())
    confirm_password = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('this username is already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('this email address is already exists')
        return email
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords must be mtach!')
        return confirm_password


class SignInForm(forms.Form):
    username = forms.CharField(max_length=77, error_messages=message, widget=forms.TextInput())
    password = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput())
    remember = forms.CharField(required=False, label='remember me', widget=forms.CheckboxInput())
    captcha = CaptchaField()