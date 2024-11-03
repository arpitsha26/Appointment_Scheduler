from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('showAppointments/', ShowAppointmentsView.as_view(), name='show_appointments'),
    path('createAppointment/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('getDoctor/', GetDoctorView.as_view(), name='get_doctor'),
    path('doctor/completed/', MarkCompletedView.as_view(), name='mark_completed'),
]

