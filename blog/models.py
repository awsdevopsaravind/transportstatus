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
    
    def __str__(self):
        return self.vehicle_owner_name

class VehicleDetails(models.Model):
    vehicle_number = models.CharField(max_length=10, null=False, blank=False)
    #owner_name = models.CharField(max_length=200, null=False, blank=False)
    owner_name = models.ForeignKey(TransporterDetails, on_delete=models.SET_NULL, null=True, blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=False, blank=False)
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    driver_phone_number = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=True, blank=True)
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
    quarry_owner_name = models.ForeignKey(QuarryDetails, on_delete=models.SET_NULL, null=True, blank=False)
    load_type = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=False)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    royalty_image_front = models.ImageField(null=False, blank=False)
    royalty_image_back = models.ImageField(null=False, blank=True)
    qty_ton = models.FloatField(null=False, blank=False, default=0.0)
    waybill_image_front = models.ImageField(null=False, blank=False)
    waybill_image_back = models.ImageField(null=False, blank=True)
    verifiedbyengineer = models.CharField(max_length=200, blank=False, null=False, choices=STATUS, default='No')
    verifiedbymalli = models.CharField(max_length=200, blank=False, null=False, choices=STATUS, default='No')
    qty_ton = models.FloatField(null=False,default=0, blank=False)
    waybill_image_front = models.ImageField(default='logo.png',null=False, blank=False)
    waybill_image_back = models.ImageField( null=False, blank=True)
    verifiedbysuresh = models.CharField(max_length=200, blank=False, null=False, choices=VERIFY, default='No')
    comments = models.CharField(max_length=200, blank=True, null=True)


class VehiclePayments(models.Model):
    vehicle_number = models.ForeignKey(VehicleDetails, on_delete=models.SET_NULL, null=True, blank=False)
    advance_given_date = models.ForeignKey(LayerWiseTripDetails, on_delete=models.SET_NULL, null=True, blank=False)
    remarks = models.CharField(max_length=200,null=False, blank=False)
    amount_given = models.FloatField(null=False, blank=False)

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