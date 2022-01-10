from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import Offering, Profile

class OfferForm(ModelForm):
    class Meta:
        model = Offering
        fields = '__all__'
        exclude = ['providerID']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class MyRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def save(self, commit=True):
        user = super(MyRegisterForm,self).save(commit=False)
        if commit:
            user.save()
        return user