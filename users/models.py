from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
import secrets


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self) -> str:
        return self.email or ''



class ConfirmCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    confirm_code = models.CharField(max_length=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.confirm_code:
            self.confirm_code = f"{secrets.randbelow(900000) + 100000}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.confirm_code