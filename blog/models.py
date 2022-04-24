from math import floor
from secrets import choice
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator


class District(models.Model):
    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    name = models.CharField(max_length=100, null=False, blank=False)
    housecount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name
        
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='logo.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description

class TransporterDetails(models.Model):
    vehicle_owner_name = models.CharField(max_length=100, null=False, blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    owner_phone_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=False, blank=False)
    rate_per_tonne = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.vehicle_owner_name

class VehicleDetails(models.Model):
    vehicle_number = models.CharField(max_length=10, null=False, blank=False)
    owner_name = models.ForeignKey(TransporterDetails, on_delete=models.SET_NULL, null=True, blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    driver_phone_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=True, blank=True)
    driver_name2 = models.CharField(max_length=200, null=True, blank=True)
    driver_phone_number2 = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=True, blank=True)
    rate_per_tonne = models.CharField(max_length=200, null=False, blank=False)
    
    def __str__(self):
        return self.vehicle_number

class LoadType(models.Model):
    load_type = models.CharField(max_length=100, null=False, blank=False)
    load_type_rate_per_tonne = models.FloatField(null=False, blank=True)
    
    def __str__(self):
        return self.load_type

class CompanyName(models.Model):
    company_name = models.CharField(max_length=100, null=False, blank=False)

    
    def __str__(self):
        return self.company_name

class QuarryDetails(models.Model):
    quarry_owner_name = models.CharField(max_length=100, null=False, blank=False)
    quarry_ton_rate = models.FloatField(null=False, blank=True)
    
    def __str__(self):
        return self.quarry_owner_name

class TripDetails(models.Model):
    company_name = models.ForeignKey(CompanyName, on_delete=models.SET_NULL, null=True, blank=False)
    trip_date = models.DateField(null=False, blank=False)
    load_type = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=False)
    quarry_owner_name = models.ForeignKey(QuarryDetails, on_delete=models.SET_NULL, null=True, blank=False)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    vehicle_number = models.ForeignKey(
        VehicleDetails , on_delete=models.SET_NULL, null=True, blank=False)
    qty_ton = models.FloatField(null=False, blank=False)
    royalty_image = models.ImageField(null=False, blank=False)
    waybill_image = models.ImageField(null=False, blank=False)

class InitialTripDetails(models.Model):
    trip_date = models.DateField(null=False, blank=False)
    company_name = models.ForeignKey(CompanyName, on_delete=models.SET_NULL, null=True, blank=False)
    vehicle_number = models.ForeignKey(
        VehicleDetails , on_delete=models.SET_NULL, null=True, blank=False)
    driver_name = models.ForeignKey(
        TransporterDetails , on_delete=models.SET_NULL, null=True, blank=False)
    quarry_owner_name = models.ForeignKey(QuarryDetails, on_delete=models.SET_NULL, null=True, blank=False)
    load_type = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=False)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    royalty_image_front = models.ImageField(null=False, blank=False)
    royalty_image_back = models.ImageField(null=False, blank=True)

class Layer2TripDetails(models.Model):
    Yes = 1
    No = 2
    STATUS = (
       (Yes, ('Confirm Send')),
       (No, ('No, require more time')),
   )
    
    trip_date = models.DateField(null=False, blank=False)
    company_name = models.ForeignKey(CompanyName, on_delete=models.SET_NULL, null=True, blank=False)
    vehicle_number = models.ForeignKey(
        VehicleDetails , on_delete=models.SET_NULL, null=True, blank=False)
    driver_name = models.ForeignKey(
        TransporterDetails , on_delete=models.SET_NULL, null=True, blank=False)
    quarry_owner_name = models.ForeignKey(QuarryDetails, on_delete=models.SET_NULL, null=True, blank=False)
    load_type = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=False)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    royalty_image_front = models.ImageField(null=False, blank=False)
    royalty_image_back = models.ImageField(null=False, blank=True)
    qty_ton = models.FloatField(null=False, blank=False)
    waybill_image_front = models.ImageField(null=False, blank=False)
    waybill_image_back = models.ImageField(null=False, blank=True)
    sendtomalli = models.PositiveSmallIntegerField(
       choices=STATUS,
       default=Yes,
   )



STATUS = [
       ('Yes', 'Data is Correct, Send Forward'),
       ('No', 'Data is wrong, Send Back'),
    ]
VERIFY = [
       ('Yes', 'Data is Correct, Verify'),
       ('No', 'Data is wrong, Send back'),
    ]
class LayerWiseTripDetails(models.Model): 
    trip_date = models.DateField(null=False, blank=False,default='2022-03-20')
    company_name = models.ForeignKey(CompanyName, on_delete=models.SET_NULL, null=True, blank=False)
    
    vehicle_owner_name = models.ForeignKey(
        TransporterDetails , on_delete=models.SET_NULL, null=True, blank=False)
    vehicle_number = models.ForeignKey(
        VehicleDetails , on_delete=models.SET_NULL, null=True, blank=False)
    driver_name = models.CharField(max_length=200,null=True, blank=False)
    # add driver phone number field details if required
    #driver_phone_number = models.CharField(max_length=200, blank=True, null=True)
    quarry_owner_name = models.ForeignKey(QuarryDetails, on_delete=models.SET_NULL, null=True, blank=False)
    load_type = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=False)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    royalty_image_front = models.ImageField(null=False, blank=False)
    royalty_image_back = models.ImageField(null=False, blank=True)
    qty_ton = models.FloatField(null=False, blank=False, default=0.0)
    waybill_image_front = models.ImageField(null=False, blank=False)
    waybill_image_back = models.ImageField(null=False, blank=True)
    #verifiedbyengineer = models.CharField(max_length=200, blank=False, null=False, choices=STATUS, default='No')
    verifiedbymalli = models.CharField(max_length=200, blank=False, null=False, choices=STATUS, default='No')
    qty_ton = models.FloatField(null=False,default=0, blank=False)
    waybill_image_front = models.ImageField(default='logo.png',null=False, blank=False)
    waybill_image_back = models.ImageField( null=False, blank=True)
    verifiedbysuresh = models.CharField(max_length=200, blank=False, null=False, choices=VERIFY, default='No')
    comments = models.CharField(max_length=200, blank=True, null=True)
    forwarded = models.CharField(max_length=200, blank=True, null=True, default='No')
    approved = models.CharField(max_length=200, blank=True, null=True,  default='No')
    verified = models.CharField(max_length=200, blank=True, null=True,  default='No')

    @property
    def qty_m3_actual_submit(self):
        return round(self.qty_ton/1.5,2)
    @property
    def qty_m3_pending(self):
        return round((self.qty_m3_actual_submit - self.qty_m3),2)
    @property
    def rate_ton(self):
        return self.load_type.load_type_rate_per_tonne
    @property
    def trip_amount(self):
        return self.qty_ton*self.load_type.load_type_rate_per_tonne

    @property
    def tax_amount(self):
        return round((self.trip_amount/100)*5,2)
    @property
    def trip_total_amount(self):
        return self.trip_amount+ self.tax_amount
    @property
    def round_off_amount(self):
        abc = self.trip_total_amount-floor(self.trip_total_amount)
        bcd =round(abc,2)
        return bcd
    @property
    def floor_amount(self):
        return round((self.trip_total_amount-self.round_off_amount),2)
    @property
    def amount_in_words(self):
        return round((self.trip_total_amount-self.round_off_amount))
    
    # fields for vehicle owners payments
    @property
    def vehicle_owner_amount(self):
        return float(self.qty_ton)*float(self.vehicle_number.rate_per_tonne)
    @property
    def vehicle_tax_amount(self):
        return round((self.vehicle_owner_amount/100)*5,2)
    @property
    def vehicle_trip_total_amount(self):
        return self.vehicle_owner_amount+ self.vehicle_tax_amount
    @property
    def vehicle_round_off_amount(self):
        abcd = self.vehicle_trip_total_amount-floor(self.vehicle_trip_total_amount)
        bcde =round(abcd,2)
        return bcde
    @property
    def vehicle_floor_amount(self):
        return round((self.vehicle_trip_total_amount-self.vehicle_round_off_amount),2)
    
        # fields for quarry owners payments
    @property
    def quarry_owner_amount(self):
        return float(self.qty_ton)*float(self.quarry_owner_name.quarry_ton_rate)
    @property
    def quarry_tax_amount(self):
        return round((self.quarry_owner_amount/100)*5,2)
    @property
    def quarry_trip_total_amount(self):
        return self.quarry_owner_amount+ self.quarry_tax_amount
    @property
    def quarry_round_off_amount(self):
        abcde = self.quarry_trip_total_amount-floor(self.quarry_trip_total_amount)
        bcdef =round(abcde,2)
        return bcdef
    @property
    def quarry_floor_amount(self):
        return round((self.quarry_trip_total_amount-self.quarry_round_off_amount),2)



class exceldata1(models.Model):
    trip_date1 = models.DateField(null=False, blank=False)
    invoice_date = models.DateField(null=False, blank=False)
    invoice_number =models.IntegerField(null=False, blank=False)
    vehicle_number = models.CharField(max_length=200,null=False, blank=False)
    material = models.CharField(max_length=200,null=False, blank=False)
    qty_ton = models.FloatField(null=False, blank=False)
    rate_ton = models.FloatField(null=False, blank=False)
    total_amount = models.FloatField(null=False, blank=False)
    tax_amount = models.FloatField(null=False, blank=False)
    total_amount_rounded = models.FloatField(null=False, blank=False)
    total_amount_decimal = models.FloatField(null=False, blank=False)
    round_off = models.FloatField(null=False, blank=False)

AMOUNTTYPE = [
       ('Advance', 'Advance'),
       ('Payment', 'Payment'),
    ]
class VehiclePayments(models.Model):
    vehicle_owner_name = models.ForeignKey(
        TransporterDetails , on_delete=models.SET_NULL, null=True, blank=False)
    vehicle_number = models.ForeignKey(VehicleDetails, on_delete=models.SET_NULL, null=True, blank=True)
    amount_type = models.CharField(max_length=200, blank=False, null=False, choices=AMOUNTTYPE, default='Advance')
    advance_given_date = models.DateField( null=False, blank=False)
    amount_given = models.FloatField(null=False, blank=False)
    remarks = models.CharField(max_length=200,null=False, blank=False)
    amount_receipt = models.ImageField( null=False, blank=True)

class QuarryPayments(models.Model):
    quarry_owner_name = models.ForeignKey(
        QuarryDetails , on_delete=models.SET_NULL, null=True, blank=False)
    amount_type = models.CharField(max_length=200, blank=False, null=False, choices=AMOUNTTYPE, default='Advance')
    amount_given_date = models.DateField( null=False, blank=False)
    amount_given = models.FloatField(null=False, blank=False)
    remarks = models.CharField(max_length=200,null=False, blank=False)
    amount_receipt = models.ImageField( null=False, blank=True)

class CompanyPayments(models.Model):
    company_name = models.ForeignKey(
        CompanyName , on_delete=models.SET_NULL, null=True, blank=False)
    amount_type = models.CharField(max_length=200, blank=False, null=False, choices=AMOUNTTYPE, default='Advance')
    amount_received_date = models.DateField( null=False, blank=False)
    amount_received = models.FloatField(null=False, blank=False)
    remarks = models.CharField(max_length=200,null=False, blank=False)
    amount_receipt = models.ImageField( null=False, blank=True)



from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name