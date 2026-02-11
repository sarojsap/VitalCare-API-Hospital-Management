from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email Field Must Be Set.")
        
        # normalise email
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return User
        

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.RoleOption.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):

    class RoleOption(models.TextChoices):
        DOCTOR = 'doctor', 'Doctor'
        PATIENT = 'patient', 'Patient'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    role = models.CharField(max_length=8, choices=RoleOption.choices, default=RoleOption.PATIENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
    def __str__(self):
        return self.email


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    insurance_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    medical_history_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Patient:{self.user.email}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualifications = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Doctor:{self.user.email}"