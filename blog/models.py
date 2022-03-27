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

class VehicleDetails(models.Model):
    vehicle_number = models.CharField(max_length=10, null=False, blank=False)
    owner_name = models.CharField(max_length=200, null=False, blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phonenumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=False, blank=False)
    rate_per_tonne = models.CharField(max_length=200, null=False, blank=False)
    
    def __str__(self):
        return self.vehicle_number

class LoadType(models.Model):
    load_type = models.CharField(max_length=100, null=False, blank=False)
    load_type_rate_per_tonne = models.FloatField(null=False, blank=True)
    
    def __str__(self):
        return self.load_type

class TripDetails(models.Model):
    '''LOADTYPE = (
			('1 kg - 1 Tonne', '1 kg - 1 Tonne'),
			('1 Tonne - 3 Tonne', '1 Tonne - 3 Tonne'),
            ('3 Tonne - 5 Tonne', '3 Tonne - 5 Tonne'),
			)'''
    trip_date = models.DateField(null=False, blank=False)
    loadtype = models.ForeignKey(LoadType, on_delete=models.SET_NULL, null=True, blank=True)
    #loadtype = models.CharField(max_length=200, null=True, blank=True, choices=LOADTYPE)
    tf_number = models.CharField(max_length=200, null=False, blank=False)
    qty_m3 = models.FloatField(null=False, blank=False)
    vehicle_number = models.ForeignKey(
        VehicleDetails , on_delete=models.SET_NULL, null=True, blank=False)
    qty_ton = models.FloatField(null=False, blank=False)
    royalty_image = models.ImageField(null=False, blank=True)
    waybill_image = models.ImageField(null=False, blank=True)
	
class VehiclePayments(models.Model):
    vehicle_number = models.ForeignKey(VehicleDetails, on_delete=models.SET_NULL, null=True, blank=True)
    advance_given_date = models.DateField(null=False, blank=False)
    remarks = models.CharField(max_length=200,null=False, blank=False)
    amount_given = models.FloatField(null=False, blank=False)

'''class TripDetailsNew(models.Model):
    trip_date = models.DateField()
    qty_m3 = models.FloatField(null=False, blank=False)
    '''