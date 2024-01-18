from rest_framework import serializers
from .models import User, Doctor, Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        errors = {}

        # Custom validation for first_name, last_name, and role
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role')

        if not first_name:
            errors['first_name'] = 'First name is required.'

        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if role not in [choice[0] for choice in User.Role.choices]:
            errors['role'] = 'Invalid role value.'

        if errors:
            raise serializers.ValidationError(errors)

        return data


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'user', 'speciality', 'years_of_experience', 'medical_license_number', 'country_of_issue', 'year_of_issue',
            'diabetes_management_experience', 'treatement_approach', 'contact_hours',
            'communication_method_for_patient', 'tel_number', 'emergency_consultations')

    def validate(self, data):
        errors = {}

        # Add custom validation for speciality (example: it should not be empty)
        speciality = data.get('speciality')
        if not speciality:
            errors['speciality'] = 'Speciality cannot be empty.'

        # Add custom validation for years_of_experience (example: it should be a positive integer)
        years_of_experience = data.get('years_of_experience')
        if not years_of_experience or not years_of_experience.isdigit() or int(years_of_experience) < 0:
            errors['years_of_experience'] = 'Years of experience should be a positive integer.'

        # Add custom validation for medical_license_number (example: it should not be empty)
        medical_license_number = data.get('medical_license_number')
        if not medical_license_number:
            errors['medical_license_number'] = 'Medical license number cannot be empty.'

        # Add similar custom validation for other fields as needed

        if errors:
            raise serializers.ValidationError(errors)

        return data


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
