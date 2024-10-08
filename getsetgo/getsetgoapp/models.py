from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VehicleCategory(models.Model):
    name = models.CharField(max_length=50) 

    class Meta:
        db_table = 'vehicle_category'

    def __str__(self):
        return self.name



class Vehicle(models.Model):
    img=models.ImageField(upload_to='image',default='')
    v_name=models.CharField(max_length=30)
    v_model=models.CharField(max_length=30)
    v_fueltype=models.CharField(max_length=20)
    v_rate=models.CharField(max_length=30)
    v_category=models.ForeignKey(VehicleCategory,on_delete=models.CASCADE)

    class Meta:
        db_table='vehicle'

    def __str__(self):
        return self.v_name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    trip_date = models.DateField()
    return_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Added field for payment ID

    class Meta:
        db_table = 'booking'


class S_Email(models.Model):
    s_email=models.CharField(max_length=30)

    class Meta:
        db_table='s_email'

