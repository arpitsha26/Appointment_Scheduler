from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('showAppointments/', Showappointments.as_view(), name='show_appointments'),
    path('createAppointment/', Createappointment.as_view(), name='create_appointment'),
    path('getDoctor/', Getdoctor.as_view(), name='get_doctor'),
    path('doctor/completed/', Markcompleted.as_view(), name='mark_completed'),
]

