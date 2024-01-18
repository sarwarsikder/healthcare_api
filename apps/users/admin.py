from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Patient
from django.core.exceptions import ValidationError


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'role')}
         ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class DoctorAdminForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    list_display = ('user', 'speciality', 'years_of_experience', 'medical_license_number')
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    list_filter = ['speciality', 'years_of_experience']

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form based on the user's role
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.user.role != 'doctor':
            # If the user's role is not "doctor," remove the user field from the form
            form.base_fields.pop('user')
        return form

    def save_model(self, request, obj, form, change):
        # Check if the user has the role of "doctor" before saving the doctor model
        if obj.user.role == 'doctor':
            super().save_model(request, obj, form, change)
        else:
            # If the user role is not "doctor," raise a validation error
            raise ValidationError('Only users with the role of "doctor" can be created as doctors.')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_of_diabetes', 'date_of_diagnosis', 'current_diabetes_medication')
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    list_filter = ['type_of_diabetes', 'date_of_diagnosis']

    def save_model(self, request, obj, form, change):
        # Check if the user has the role of "patient" before saving the patient model
        if obj.user.role == 'patient':
            super().save_model(request, obj, form, change)
        else:
            # If the user role is not "patient", raise a validation error
            raise ValidationError('Only users with the role of "patient" can be created as patients.')


# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
# Register the Doctor model with the custom DoctorAdmin
admin.site.register(Doctor, DoctorAdmin)
# Register the Patient model with the custom PatientAdmin
admin.site.register(Patient, PatientAdmin)
