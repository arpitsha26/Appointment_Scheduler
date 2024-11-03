from django.contrib import admin
from Appointment_Webapp.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Doctoravailability)