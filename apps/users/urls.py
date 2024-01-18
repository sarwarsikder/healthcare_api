from django.urls import path
from .views import register_user, doctor_create, patient_create, get_user_profile, get_doctor_details, \
    get_patient_details, update_doctor_details, update_patient_details, user_details

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('doctor/create/', doctor_create, name='doctor_create'),
    path('patient/create/', patient_create, name='patient_create'),
    path('user/profile/', get_user_profile, name='get_user_profile'),
    path('doctor/details/', get_doctor_details, name='get_doctor_details'),
    path('patient/details/', get_patient_details, name='get_patient_details'),
    path('doctor/details/update/', update_doctor_details, name='update_doctor_details'),
    path('patient/details/update/', update_patient_details, name='update_patient_details'),
    path('profile/details/', user_details, name='user_details'),
]
