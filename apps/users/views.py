from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Doctor, Patient, User
from .serializers import UserSerializer, DoctorSerializer, PatientSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user_id': user.id},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def doctor_create(request):
    try:
        # Check if 'user' is present in the request data
        user_instance = request.user

        try:
            # Try to get an existing Doctor instance
            doctor_instance = Doctor.objects.get(user=user_instance)
            # If 'user' is present, it's an edit operation
            serializer = DoctorSerializer(doctor_instance, data=request.data, partial=True)
        except Doctor.DoesNotExist:
            # If 'user' is not present, it's a create operation
            serializer = DoctorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user_instance)  # Set the user when saving
            return Response({'message': 'Profile created/updated successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def patient_create(request):
    try:
        # Check if 'user' is present in the request data
        user_instance = request.user

        try:
            # Try to get an existing Patient instance
            patient_instance = Patient.objects.get(user=user_instance)
            # If 'user' is present, it's an edit operation
            serializer = PatientSerializer(patient_instance, data=request.data, partial=True)
        except Patient.DoesNotExist:
            # If 'user' is not present, it's a create operation
            serializer = PatientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user_instance)  # Set the user when saving
            return Response({'message': 'Profile created/updated successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user  # Use request.user directly
        serializer = UserSerializer(user)
        return Response({'message': 'Profile fetched successfully', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_details(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        serializer = DoctorSerializer(doctor)
        return Response({'message': 'Doctor details fetched successfully', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor details not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_details(request):
    try:
        patient = Patient.objects.get(user=request.user)
        serializer = PatientSerializer(patient)
        return Response({'message': 'Patient details fetched successfully', 'data': serializer.data},
                        status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'error': 'Patient details not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_doctor_details(request):
    try:
        print(request.user)
        print(request.data)

        doctor = Doctor.objects.get(user=request.user)

        print("RST")
        print(request.data)

        # Validate the data before updating
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)

        print("TEST")

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Doctor.DoesNotExist:
        return Response({'error': 'Profile details not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_patient_details(request):
    try:
        patient = Patient.objects.get(user=request.user)

        # Validate the data before updating
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Patient.DoesNotExist:
        return Response({'error': 'Profile details not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_details(request):
    try:
        user = User.objects.get(pk=request.user.id)

        if request.method == 'GET':
            # If it's a GET request, serialize and return the user data
            serializer = UserSerializer(user)
            return Response({'data': serializer.data, "message": "User details fetched successfully",
                             }, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            # If it's a PUT request, update the user data
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Profile updated successfully', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
