from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('createAppointment', views.create_appointment, name='create_appointment'),
    path('showAppointments', views.show_appointments, name='show_appointments'),
    path('doctor/completed/<int:appointment_id>', views.mark_appointment_completed, name='mark_appointment_completed'),
    path('admin/delete/<str:doctor_email>', views.delete_doctor, name='delete_doctor'),
    path('getDoctor', views.get_doctors, name='get_doctors'),
    path('patient/history', views.patient_history, name='patient_history'),
]
