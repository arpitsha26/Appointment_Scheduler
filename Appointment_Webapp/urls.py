from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('showAppointments/', Showappointments.as_view(), name='show_appointments'),
    path('createAppointment/', Createappointment.as_view(), name='create_appointment'),
    path('getdoctor/', Getdoctor.as_view(), name='get_doctor'),
    path('doctor/completed/', Markcompleted.as_view(), name='mark_completed'),
    path('admin/delete/', doctordelete.as_view(), name='delete_particulardoctor'),
    path('patient/history/', patienthistory.as_view(), name='patienthistory'),
    path('password/reset/', passwordreset.as_view(), name='password_rest'),
    path('password/reset/<str:token>/', resetconfirm.as_view(), name='passwordrestconfirm'),
    path('welcome', welcome.as_view(), name='welcome page')
] 

