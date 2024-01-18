from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    pass


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100, blank=False, null=False, )
    last_name = models.CharField(max_length=100, blank=False, null=False, )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Role(models.TextChoices):
        PATIENT = 'patient'
        DOCTOR = 'doctor'
        ADMIN = 'admin'

    # Identifying the user role based on this (by default it will be patient if no role assigned)
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.role + ")"

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # patients = models.ManyToManyField('Patient', related_name='treated_by_doctors', null=True)

    speciality = models.CharField(max_length=50, blank=True, null=True)
    years_of_experience = models.CharField(max_length=50, blank=True, null=True)
    medical_license_number = models.CharField(max_length=50, blank=True, null=True)
    country_of_issue = models.CharField(max_length=50, blank=True, null=True)
    year_of_issue = models.CharField(max_length=50, blank=True, null=True)

    diabetes_management_experience = models.CharField(max_length=50, blank=True, null=True)
    treatement_approach = models.CharField(max_length=50, blank=True, null=True)
    contact_hours = models.CharField(max_length=50, blank=True, null=True)
    communication_method_for_patient = models.CharField(max_length=50, blank=True, null=True)
    tel_number = models.CharField(max_length=50, blank=True, null=True)
    emergency_consultations = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return (f'Doctor {self.user.first_name} {self.user.last_name}: Specialty - {self.specialty}, Years of '
                f'Experience - {self.years_of_experience}')


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # doctors = models.ManyToManyField('Doctor', related_name='patients_treated', null=True)

    type_of_diabetes = models.CharField(max_length=50, blank=True, null=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)
    current_diabetes_medication = models.CharField(max_length=50, blank=True, null=True)
    blood_sugar_level = models.CharField(max_length=50, blank=True, null=True)
    medical_history = models.CharField(max_length=50, blank=True, null=True)
    dietary_habits = models.CharField(max_length=50, blank=True, null=True)

    physical_activity_level = models.CharField(max_length=50, blank=True, null=True)
    smoking_habits = models.CharField(max_length=50, blank=True, null=True)
    alcohol_consumption = models.CharField(max_length=50, blank=True, null=True)

    date_last_HbA1c_test_and_result = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return (f'Patient {self.user.first_name} {self.user.last_name}: Type of Diabetes - {self.type_of_diabetes}, '
                f'Date of Diagnosis - {self.date_of_diagnosis}')

    def __str__(self):
        return (
            f'Patient {self.user.first_name} {self.user.last_name}: Physical Activity Level - {self.physical_activity_level}, '
            f'Smoking Habits - {self.smoking_habits}, Alcohol Consumption - {self.alcohol_consumption}, Dietary '
            f'Habits - {self.dietary_habits}')
