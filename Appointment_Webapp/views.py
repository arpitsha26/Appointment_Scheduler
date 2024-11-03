from rest_framework import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import *
from .permissions import IsPatient, IsDoctor, IsAdmin
from .serializers import *
from django.conf import settings
import jwt
from datetime import datetime, timedelta

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            serializer.save(password=make_password(password))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(User, email=email)

        return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ShowAppointmentsView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def get(self, request):
        email = request.query_params.get('email')
        patient = get_object_or_404(User, email=email, account_type='Patient')
        appointments = Appointment.objects.filter(patient=patient, status='scheduled')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def post(self, request):
        doctor_id = request.query_params.get('doctor_id')
        doctor = get_object_or_404(User, id=doctor_id, account_type='Doctor')
        appointment_date = request.data.get('appointment_date')
        appointment = Appointment.objects.create(patient=request.user, doctor=doctor, appointment_date=appointment_date)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

class GetDoctorView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]

    def get(self, request):
        specialization = request.query_params.get('specialization')
        doctors = User.objects.filter(account_type='Doctor', specialization=specialization)
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkCompletedView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def patch(self, request):
        appointment_id = request.query_params.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
        appointment.status = 'completed'
        appointment.save()
        return Response({'message': 'Appointment marked as completed'}, status=status.HTTP_200_OK)

