import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from future.backports.datetime import timedelta
from django.contrib.auth.models import BaseUserManager


LEN_CONFIRMATION_CODE = 6

CODE_VALIDITY_MINUTES = 20


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('email should be mandatory')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(email, password, **kwargs)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=False, max_length=150)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def activate(self):
        self.is_active = True
        self.save()

class EmailConfirmation(models.Model):
    email = models.ForeignKey(to=CustomUser, to_field='email', on_delete=models.CASCADE)
    code = models.CharField(max_length=LEN_CONFIRMATION_CODE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = self._generate_code()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_code():
        return ''.join(str(random.randint(0, 9)) for _ in range(LEN_CONFIRMATION_CODE))

    def is_code_expired(self):
        return now() > self.created_at + timedelta(minutes=CODE_VALIDITY_MINUTES)

    def send_email(self):
        print(f'Send {self.code} to {self.email}')
