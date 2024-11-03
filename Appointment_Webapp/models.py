from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from .choices import *
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='Patient')
    specialization = models.CharField(max_length=100, null=True, blank=True)
    
    
    USERNAME_FIELD='email'
    
    def __str__(self):
        return self.email
    
    
    
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.CharField(max_length=10)  
    start_time = models.TimeField() 
    end_time = models.TimeField()

    