from django.forms import ModelForm, fields
from .models import Offering

class OfferForm(ModelForm):
    class Meta:
        model = Offering
        fields = '__all__'