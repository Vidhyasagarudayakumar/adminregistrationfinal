from django import forms
from .models import registration
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=1000)
    firstname = forms.CharField(label='First Name', max_length=100)
    lastname = forms.CharField(label='Last Name', max_length=100)
    phonenumber = forms.CharField(label='Phone Number' , max_length=15)
    class Meta:
        model = registration
        exclude = ['user', 'user_id','phonenumber']

    def is_valid(self):
        valid = super(RegistrationForm, self).is_valid()
        data = self.cleaned_data
        phonenumber = data['phonenumber']
        password1 = data['password1']
        password2 = data['password2']
        if len(password1)>= 6:
            pass
        else:
            valid=False
            self._errors['password1'] = [u'Password is too WEAK. It should have atleast 6 characters ']
        if password1 != password2:
            valid = False
            self._errors['password1'] = [u'Passwords does not match']
        try:
            User.objects.get(email=data['email'])
            valid = False
            self._errors['email'] = [u'This Email id is already in use']
        except User.DoesNotExist:
            pass
        try:
            User.objects.get(username=data['username'])
            valid = False
            self._errors['username'] = [u'This Username is already in use']
        except User.DoesNotExist:
            pass
        try:
            if registration.objects.get(phonenumber=data['phonenumber']):
                valid = False
                self._errors['phonenumber'] = [u'This Phone Number exist already ']


        except registration.DoesNotExist:
            if len(phonenumber) == 10:
                pass
            else:
                valid = False
                self._errors['phonenumber'] = [u'Enter Valid Number']

        return valid






class Userloginform(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput)



class changepasswordform(forms.Form):
    password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def __init__(self, user, data=None):
        self.user = user
        super(changepasswordform, self).__init__(data=data)

    def is_valid(self):
        valid = super(changepasswordform, self).is_valid()
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        password2 = data['password2']



        if password1 != password2:
            valid = False
            self._errors['password1'] = [u'Passwords does not match']
        if password1 != password:
            pass
        else:
            valid = False
            self._errors['password'] = [u' current password and new password should not be same']
        return valid