from django.forms import ModelForm, fields
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