from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class AddTripDetailsForm(forms.ModelForm):
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y'])
    class Meta:
        model = TripDetails
        fields = '__all__'

class AddVehicleDetailsForm(forms.ModelForm):
    class Meta:
        model = VehicleDetails
        fields = '__all__'

'''class AddTripDetailsFormNew(forms.ModelForm):
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y',],help_text = "Enter Date value mm/dd/yyyy")
    class Meta:
        model = TripDetailsNew
        fields = '__all__'
        '''