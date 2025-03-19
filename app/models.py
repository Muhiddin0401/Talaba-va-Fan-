from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class Fan(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Talaba(models.Model):
    ism_fam = models.CharField(max_length=50)
    sharf = models.CharField(max_length=50)
    tel_raqam = models.CharField(max_length=13, blank=True, null=True)
    manzil = models.CharField(max_length=100)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name="get_talaba", null=True, blank=True)
    views = models.IntegerField(default=0)
    fayl = models.FileField(upload_to='talaba_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.ism_fam}"

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, email=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqami kiritilishi shart!!!")
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser uchun is_superuser True bo‘lishi kerak')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser uchun is_staff True bo‘lishi kerak')

        return self.create_user(phone, password, email, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?\d{9,14}$', message='Telefon raqamni to‘g‘ri formatda kiriting')
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone