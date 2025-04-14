from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class CustomerUserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_active=True, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(phone=phone, password=password, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None,  **extra_fields):
        return self.create_user(phone=phone, password=password, is_active=True, is_staff=True, is_superuser=True)


class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'phone'

    def format(self):
        return {
            'phone': self.phone,
            'name': self.name,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,

        }