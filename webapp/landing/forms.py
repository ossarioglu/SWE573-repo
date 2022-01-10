from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import Offering, Profile

# This is custom form for listing services at front-end
class OfferForm(ModelForm):

    # Information is shown for all fields other than 'providerID' 
    class Meta:
        model = Offering
        fields = '__all__'
        exclude = ['providerID']

# This is custom form for listing profiles at front-end
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

# This is custom form for listing user information at front-end
# It's inherited from Django's default UserCreationForm
class MyRegisterForm(UserCreationForm):
    # emain, first_name, and last_name fields are shown at this form as additional to UserCreationForm
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
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