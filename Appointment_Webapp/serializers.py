
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'status', 'appointment_id']
        
class DoctoravailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctoravailability
        fields = ['day_of_week', 'start_time', 'end_time']
    
    doctor = serializers.CharField(source="doctor.first_name")
