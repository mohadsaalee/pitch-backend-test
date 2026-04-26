from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('role', 'innovator')  # default role for superusers
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('innovator', 'Innovator'),
        ('startup', 'Startup'),
        ('investor', 'Investor'),
        ('consultant', 'Consultant'),
        ('ecosystem_partner', 'Ecosystem Partner'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']   # role removed from here

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} ({self.role or "superuser"})'

    @property
    def is_private_profile(self):
        return self.role in ('innovator', 'startup')

    @property
    def is_public_profile(self):
        return self.role in ('investor', 'consultant', 'ecosystem_partner')
