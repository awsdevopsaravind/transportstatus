from faulthandler import disable
from multiprocessing import AuthenticationError
from xml.etree.ElementInclude import include
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Profile
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

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
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y', '%Y-%m-%d'])
    class Meta:
        model = TripDetails
        fields = '__all__'


class InitialTripDetailsForm(forms.ModelForm):
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y', '%Y-%m-%d'])
    class Meta:
        model = InitialTripDetails
        fields = '__all__'

class Layer2TripDetailsForm(forms.ModelForm):
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y', '%Y-%m-%d'],disabled=True)
    qty_m3 = forms.FloatField(disabled=True)
    class Meta:
        model = Layer2TripDetails
        fields = '__all__'

class Layerwise1TripDetailsForm(forms.ModelForm):
    trip_date = forms.DateField(input_formats=['%d-%m-%Y','%d/%m/%Y', '%Y-%m-%d'])
    class Meta:
        model = LayerWiseTripDetails
        fields = '__all__'
        exclude = {'qty_ton','waybill_image_front','waybill_image_back','verifiedbyengineer','verifiedbymalli','verifiedbysuresh'}

class Layerwise2TripDetailsForm(forms.ModelForm):
    class Meta:
        model = LayerWiseTripDetails
        fields = '__all__'
        exclude = {'verifiedbymalli','verifiedbysuresh'}

class Layerwise3TripDetailsForm(forms.ModelForm):
    class Meta:
        model = LayerWiseTripDetails
        fields = '__all__'
        exclude = {'verifiedbysuresh'}

class Layerwise4TripDetailsForm(forms.ModelForm):
    class Meta:
        model = LayerWiseTripDetails
        fields = '__all__'
        exclude = {'verifiedbyengineer'}


class VehiclePaymentsForm(forms.ModelForm):
    class Meta:
        model = VehiclePayments
        fields = '__all__'

class AddCompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = CompanyName
        fields = '__all__'

class AddLoadtypeDetailsForm(forms.ModelForm):
    class Meta:
        model = LoadType
        fields = '__all__'

class AddQuarryOwnerDetailsForm(forms.ModelForm):
    class Meta:
        model = QuarryDetails
        fields = '__all__'

class AddOwnerDetailsForm(forms.ModelForm):
    class Meta:
        model = TransporterDetails
        fields = '__all__'

class AddVehicleDetailsForm(forms.ModelForm):
    class Meta:
        model = VehicleDetails
        fields = '__all__'

class DailyReportForm(forms.ModelForm):
    trip_date = forms.DateField(required=True)
    class Meta:
        model = LayerWiseTripDetails
        fields = ['trip_date', 'vehicle_owner_name']

class TripSearchForm(forms.ModelForm):
   class Meta:
     model = LayerWiseTripDetails
     fields = ['trip_date', 'load_type']

class TripSearchForm_old(forms.ModelForm):
   class Meta:
     model = exceldata1
     fields = ['trip_date1', 'material']

class QuarryOwnerForm(forms.ModelForm):
   class Meta:
     model = LayerWiseTripDetails
     fields = ['trip_date', 'load_type', 'quarry_owner_name']

class DailyGstInvoicesForm(forms.ModelForm):

   class Meta:
     model = LayerWiseTripDetails
     fields = ['trip_date']


from django import forms
from .models import Person, City

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
