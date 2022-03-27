from django.contrib import admin
from .models import *

from .models import Photo, Category

admin.site.register(Category)
admin.site.register(Photo)

admin.site.register(District)
admin.site.register(Post)
admin.site.register(Profile)

admin.site.register(VehicleDetails)
admin.site.register(LoadType)
admin.site.register(TripDetails)
admin.site.register(VehiclePayments)
#admin.site.register(TripDetailsNew)