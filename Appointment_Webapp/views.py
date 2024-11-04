from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import *
from django.core.mail import send_mail
from .permissions import IsPatient, IsDoctor, IsAdmin
from .serializers import *
from django.conf import settings
import jwt
from datetime import datetime, timedelta

class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            serializer.save(password=make_password(password))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Showappointments(APIView):
    permission_classes = [IsPatient]
 
    def get(self, request):
        email = request.query_params.get('email')
        patient = get_object_or_404(User, email=email, account_type='Patient')
        appointments = Appointment.objects.filter(patient=patient, status='scheduled')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Createappointment(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request):
        doctor_id = request.query_params.get('doctor_id')
        doctor = get_object_or_404(User, id=doctor_id, account_type='Doctor')
        appointment_date = request.data.get('appointment_date')
        appointment_id=request.data.get('appointment_id')
        appointment = Appointment.objects.create(patient=request.user, doctor=doctor, appointment_date=appointment_date)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

class Getdoctor(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def get(self, request):
        specialization = request.query_params.get('specialization')
        doctors = User.objects.filter(account_type='Doctor', specialization=specialization)
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Markcompleted(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def patch(self, request):
        appointment_id = request.query_params.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
        appointment.status = 'completed'
        appointment.save()
        return Response({'message': 'Appointment completed'}, status=status.HTTP_200_OK)


class patienthistory(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({'error': 'Patient ID req'}, status=status.HTTP_400_BAD_REQUEST)
        patient = User.objects.filter(id=patient_id, account_type='Patient').first()
        if not patient:
            return Response({'error': ' not found'}, status=status.HTTP_404_NOT_FOUND)
        appointments = Appointment.objects.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class doctordelete(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def delete(self, request):
        doctor_email = request.query_params.get('email')
        if not doctor_email:
            return Response({'error': 'Doctor email  req.'}, status=status.HTTP_400_BAD_REQUEST)
        doctor = User.objects.filter(email=doctor_email, account_type='Doctor').first()
        if not doctor:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        doctor.delete()
        return Response({'message': f'Doctor with email {doctor_email} deleted'}, status=status.HTTP_200_OK)
    
class passwordreset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm='HS256')
        reset_link = f"http://127.0.0.1:8000/password/reset/{token}"
        send_mail('Password Reset Request', f'link here: {reset_link}', 'arpitsharma1263@gmail.com', [email])
        return Response({'message': ' reset link sent'}, status=status.HTTP_200_OK)

class resetconfirm(APIView):
    permission_classes = [AllowAny]
    def post(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_object_or_404(User, id=payload['user_id'])
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            })
    
class welcome(APIView):

    def get(self,request):
        try:
            return Response({
                "msg":"welcome to appointment_scheduler app"
            })
        except Exception as e:
            return Response({
                "msg":"Internal server error"
            })