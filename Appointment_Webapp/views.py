from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from django.conf import settings
import jwt
from datetime import datetime, timedelta

@csrf_exempt

@api_view(['POST'])
def signup(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(email=email, password=password)
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.save()
    
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    user = authenticate(email=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_appointment(request):
    if request.user.account_type != 'Patient':
        return Response({'error': 'Only patients can create appointments'}, status=status.HTTP_403_FORBIDDEN)

    doctor_id = request.data.get('doctor_id')
    appointment_date = request.data.get('appointment_date')

    try:
        doctor = User.objects.get(id=doctor_id, account_type='Doctor')
    except User.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    appointment = Appointment.objects.create(
        patient=request.user,
        doctor=doctor,
        appointment_date=appointment_date,
        status='scheduled'
    )
    return Response({'message': 'Appointment created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_appointments(request):
    if request.user.account_type != 'Patient':
        return Response({'error': 'Only patients can view appointments'}, status=status.HTTP_403_FORBIDDEN)

    appointments = Appointment.objects.filter(patient=request.user, status='scheduled')
    appointment_data = [{'doctor': appointment.doctor.id, 'date': appointment.appointment_date, 'status': appointment.status} for appointment in appointments]
    return Response(appointment_data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_appointment_completed(request, appointment_id):
    if request.user.account_type != 'Doctor':
        return Response({'error': 'Only doctors can mark appointments as completed'}, status=status.HTTP_403_FORBIDDEN)

    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user)
        appointment.status = 'completed'
        appointment.save()
        return Response({'message': 'Appointment marked as completed'}, status=status.HTTP_200_OK)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_doctor(request, doctor_email):
    if request.user.account_type != 'Admin':
        return Response({'error': 'Only admins can delete doctors'}, status=status.HTTP_403_FORBIDDEN)

    try:
        doctor = User.objects.get(email=doctor_email, account_type='Doctor')
        doctor.delete()
        return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors(request):
    if request.user.account_type != 'Patient':
        return Response({'error': 'Only patients can access this route'}, status=status.HTTP_403_FORBIDDEN)
    
    specialization = request.query_params.get('specialization')
    if not specialization:
        return Response({'error': 'Specialization query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    doctors = User.objects.filter(account_type='Doctor', specialization=specialization)
    doctor_data = [{
        'id': doctor.id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'email': doctor.email,
        'specialization': doctor.specialization
    } for doctor in doctors]

    return Response(doctor_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_availability(request):
    if request.user.account_type != 'Patient':
        return Response({'error': 'Only patients can access this route'}, status=status.HTTP_403_FORBIDDEN)
    
    doctor_id = request.query_params.get('doctor_id')
    if not doctor_id:
        return Response({'error': 'Doctor ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doctor = User.objects.get(id=doctor_id, account_type='Doctor')
    except User.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    availability = DoctorAvailability.objects.filter(doctor=doctor)
    if not availability.exists():
        return Response({'message': 'No availability found for this doctor'}, status=status.HTTP_404_NOT_FOUND)
    
    availability_data = DoctorAvailabilitySerializer(availability, many=True).data

    return Response({
        'doctor': f"{doctor.first_name} {doctor.last_name}",
        'availability': availability_data
    }, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_history(request):
    return